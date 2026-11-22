"""Distill the freeform composer: run real requests through the freeform pathway with a big
teacher model, keep the accepted Express, and write chat-format training data.

    uv run python scripts/distill.py --n 40                    # smoke test
    uv run python scripts/distill.py --n 1200 --workers 4      # a training set (resumable)
    uv run python scripts/distill.py --prompts my_prompts.txt  # your own requests, one per line

Teacher: Claude by default (ANTHROPIC_API_KEY), or any OpenAI-compatible model if
A2UI_APPS_PLANNER_URL is set (e.g. Kimi on Ollama Cloud, https://ollama.com/v1).

Every example is the teacher's *accepted* reply: the pathway validated it against
the pruned catalog (and repaired it if needed) exactly as it does at runtime. The
training prompt is `slim_system(...)`, the same prompt RoutedLLM sends the composer.

Writes to training/data/: requests.jsonl, examples.jsonl, rejects.jsonl, train.jsonl, val.jsonl.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import random
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from a2ui_apps.composer import RecordingLLM, openai_from_env, slim_system
from a2ui_apps.llm import LLM, AnthropicLLM
from a2ui_apps.pathways.base import PathwayFailed
from a2ui_apps.pathways.freeform import FreeformPathway
from a2ui_apps.sdk import AppState

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "training" / "data"

DOMAINS = [
    "B2B SaaS analytics", "consumer fintech", "telehealth clinic", "fashion e-commerce", "online courses",
    "HR and recruiting", "marketing agency", "real estate listings", "travel booking", "nonprofit donations",
    "developer API platform", "logistics", "restaurant ordering", "fitness studio", "insurance claims",
    "event ticketing", "legal practice", "media publisher", "IoT fleet", "cybersecurity", "property management",
    "creator newsletters", "university admissions", "pet care", "community bank",
]
SURFACES = [
    "marketing landing page with hero, features and a call to action", "pricing page with three plans",
    "sign-in screen", "multi-step onboarding wizard", "account settings with tabs", "user profile page",
    "checkout form", "FAQ page", "empty state for a list with no results", "help center home",
    "team directory with avatars and roles", "order detail view with status and line items",
    "notification center", "file upload screen", "preferences form with toggles and selects",
    "product detail page", "event schedule", "comparison of two options", "status page for services",
    "booking confirmation", "KPI overview with a chart and a table", "contact page with a form and office details",
    "blog article page", "changelog / release notes", "admin table with filters and row actions",
]
VOICES = [
    "terse, like a ticket title", "a casual one-line ask", "a detailed spec with exact fields and copy",
    "a designer describing layout and hierarchy", "a founder describing what users should be able to do",
]
VIEWPORTS = [{"width": 390, "height": 844}, {"width": 820, "height": 1180}, {"width": 1440, "height": 900}]


class Requests(BaseModel):
    requests: list[str]


def teacher_from_env(name: str) -> LLM:
    if name == "claude":
        return AnthropicLLM()
    llm = openai_from_env("A2UI_APPS_PLANNER")
    if llm is None:
        sys.exit("--teacher env needs A2UI_APPS_PLANNER_URL (and _MODEL, _KEY)")
    return llm


def key(text: str) -> str:
    return hashlib.sha1(" ".join(text.lower().split()).encode()).hexdigest()[:16]


def write_requests(teacher: LLM, n: int, seed: int, seen: set[str]) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    combos = list(itertools.product(DOMAINS, SURFACES))
    rng.shuffle(combos)
    out: list[dict[str, Any]] = []
    for domain, surface in itertools.cycle(combos):
        if len(out) >= n:
            break
        voices = rng.sample(VOICES, 3)
        try:
            batch = teacher.structured(
                task="distill.requests",
                system=["You write realistic requests that people send to an AI app builder."],
                prompt=(f"Write 3 different requests for a {surface} for a {domain} product, one in each voice: "
                        f"{'; '.join(voices)}. Vary the specifics (names, fields, numbers, copy). "
                        "Do not mention design systems, components or JSON."),
                schema=Requests,
                effort="low",
            )
        except Exception as e:
            print(f"  request batch failed: {e}", file=sys.stderr)
            continue
        for text in batch.requests:
            if len(text) > 8 and (k := key(text)) not in seen:
                seen.add(k)
                out.append({"id": k, "prompt": text.strip(), "domain": domain, "surface": surface})
        print(f"  requests {len(out)}/{n}", file=sys.stderr)
    return out[:n]


def compose(teacher: LLM, item: dict[str, Any], rng: random.Random) -> dict[str, Any]:
    """Run the real freeform pathway with the teacher; return a training example or a rejection."""
    rec = RecordingLLM(teacher)
    context = {"getViewport": rng.choice(VIEWPORTS)} if rng.random() < 0.3 else None
    runner = FreeformPathway().run(item["prompt"], rec, surface_id="app", state=AppState(), context=context)
    try:
        while True:
            next(runner)
    except StopIteration as done:
        slots = done.value
    except PathwayFailed as e:
        return {**item, "rejected": True, "errors": [str(x)[:300] for x in (e.errors or [str(e)])][:10]}
    call = rec.last("freeform.generate")
    selection = rec.last("freeform.select")
    system = "\n\n".join(slim_system(call["system"]))
    user = call["messages"][0]["content"]
    return {
        **item,
        "rejected": False,
        "attempts": slots.attempts,
        "selection": selection["result"]["components"] if selection else [],
        "context": context,
        "est_tokens": (len(system) + len(user) + len(call["reply"])) // 3.6,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
            {"role": "assistant", "content": call["reply"]},
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--n", type=int, default=1200, help="requests to attempt")
    parser.add_argument("--prompts", type=Path, help="use these requests (one per line) instead of generating them")
    parser.add_argument("--teacher", choices=["auto", "claude", "env"], default="auto")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--max-tokens", type=int, default=7600, help="drop examples longer than this (training context is 8k)")
    parser.add_argument("--val-frac", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args(argv)

    name = args.teacher if args.teacher != "auto" else ("env" if os.environ.get("A2UI_APPS_PLANNER_URL") else "claude")
    teacher = teacher_from_env(name)
    args.out.mkdir(parents=True, exist_ok=True)
    req_path, ex_path, rej_path = (args.out / f for f in ("requests.jsonl", "examples.jsonl", "rejects.jsonl"))

    requests = [json.loads(line) for line in req_path.open()] if req_path.exists() else []
    seen = {r["id"] for r in requests}
    if args.prompts:
        new = [{"id": key(p), "prompt": p.strip()} for p in args.prompts.read_text().splitlines() if p.strip()]
        new = [r for r in new if r["id"] not in seen]
    elif len(requests) < args.n:
        print(f"Writing {args.n - len(requests)} requests with the {name} teacher...", file=sys.stderr)
        new = write_requests(teacher, args.n - len(requests), args.seed + len(requests), seen)
    else:
        new = []
    with req_path.open("a") as f:
        for r in new:
            f.write(json.dumps(r) + "\n")
    requests += new

    done: set[str] = set()
    for p in (ex_path, rej_path):
        if p.exists():
            done |= {json.loads(line)["id"] for line in p.open()}
    todo = [r for r in requests if r["id"] not in done]
    print(f"Composing {len(todo)} ({len(done)} done) with {args.workers} workers", file=sys.stderr)

    lock = threading.Lock()
    kept = rejected = 0
    with ThreadPoolExecutor(args.workers) as pool, ex_path.open("a") as fx, rej_path.open("a") as fr:
        futures = {pool.submit(compose, teacher, r, random.Random(f"{args.seed}{r['id']}")): r for r in todo}
        for future in as_completed(futures):
            try:
                row = future.result()
            except Exception as e:  # refusals, transport errors: skip, keep going
                row = {**futures[future], "rejected": True, "errors": [f"{type(e).__name__}: {e}"[:300]]}
            with lock:
                if row["rejected"]:
                    rejected += 1
                    fr.write(json.dumps(row) + "\n")
                    fr.flush()
                else:
                    kept += 1
                    fx.write(json.dumps(row) + "\n")
                    fx.flush()
                print(f"  kept {kept}  rejected {rejected}", file=sys.stderr)

    examples = [json.loads(line) for line in ex_path.open()] if ex_path.exists() else []
    usable = [e for e in examples if e["est_tokens"] <= args.max_tokens]
    rng = random.Random(args.seed)
    rng.shuffle(usable)
    n_val = max(1, int(len(usable) * args.val_frac)) if len(usable) >= 20 else 0
    for split, rows in (("val", usable[:n_val]), ("train", usable[n_val:])):
        with (args.out / f"{split}.jsonl").open("w") as f:
            for e in rows:
                f.write(json.dumps({k: e[k] for k in ("id", "prompt", "selection", "context", "attempts", "messages")}) + "\n")
    first_try = sum(e["attempts"] == 1 for e in examples)
    print(f"{len(usable) - n_val} train / {n_val} val -> {args.out}  "
          f"(teacher first-try {first_try}/{len(examples)}, {len(examples) - len(usable)} too long)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
