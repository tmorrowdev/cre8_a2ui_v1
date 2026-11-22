"""Score a composer on held-out requests through the real freeform pathway.

    uv run python scripts/eval_composer.py --url https://you--cre8-a2ui-composer-server.modal.run/v1 --key $KEY
    uv run python scripts/eval_composer.py --teacher claude      # baseline: the big model, full prompt

Uses training/data/val.jsonl from scripts/distill.py. The teacher's recorded
component selection is replayed, so only the compose step is measured and no
planner calls are made. Repairs stay on the model under test (no escalation),
so "first try" and "within 3" are the composer's own numbers.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

from a2ui_apps.composer import ReplaySelection, RoutedLLM
from a2ui_apps.llm import AnthropicLLM, OpenAICompatLLM
from a2ui_apps.pathways.base import PathwayFailed
from a2ui_apps.pathways.freeform import FreeformPathway
from a2ui_apps.sdk import AppState

ROOT = Path(__file__).resolve().parent.parent


def run_one(row: dict[str, Any], make_llm) -> dict[str, Any]:
    llm = make_llm(row["selection"])
    t0 = time.time()
    errors: list[str] = []
    runner = FreeformPathway().run(row["prompt"], llm, surface_id="app", state=AppState(), context=row.get("context"))
    try:
        while True:
            event = next(runner)
            if event.get("step", {}).get("name") == "repair":
                errors.append(event["step"]["detail"].split(": ", 1)[-1])
    except StopIteration as done:
        return {"id": row["id"], "ok": True, "attempts": done.value.attempts, "latency": time.time() - t0, "errors": errors}
    except PathwayFailed:
        return {"id": row["id"], "ok": False, "attempts": 3, "latency": time.time() - t0, "errors": errors}
    except Exception as e:
        return {"id": row["id"], "ok": False, "attempts": 0, "latency": time.time() - t0, "errors": [f"{type(e).__name__}: {e}"]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--url", help="OpenAI-compatible base URL of the composer (…/v1)")
    parser.add_argument("--model", default="a2ui-composer")
    parser.add_argument("--key")
    parser.add_argument("--teacher", choices=["claude"], help="evaluate the big model with the full prompt instead")
    parser.add_argument("--data", type=Path, default=ROOT / "training" / "data" / "val.jsonl")
    parser.add_argument("--limit", type=int, default=40)
    args = parser.parse_args(argv)

    rows = [json.loads(line) for line in args.data.open()][: args.limit]
    if args.teacher:
        teacher = AnthropicLLM()
        make_llm = lambda sel: ReplaySelection(sel, inner=teacher)  # noqa: E731
        label = f"teacher {teacher.model}"
    else:
        if not args.url:
            parser.error("--url is required unless --teacher is given")
        composer = OpenAICompatLLM(base_url=args.url, model=args.model, api_key=args.key, max_tokens=4096)
        make_llm = lambda sel: RoutedLLM(planner=ReplaySelection(sel), composer=composer, escalate_repairs=False)  # noqa: E731
        label = f"composer {args.model}"

    results = []
    for i, row in enumerate(rows, 1):  # sequential: latency numbers stay honest
        results.append(run_one(row, make_llm))
        r = results[-1]
        print(f"[{i}/{len(rows)}] {'ok ' if r['ok'] else 'BAD'} try {r['attempts']} {r['latency']:.1f}s  {row['prompt'][:60]}", file=sys.stderr)

    n = len(results)
    first = sum(r["ok"] and r["attempts"] == 1 for r in results)
    final = sum(r["ok"] for r in results)
    lat = sorted(r["latency"] for r in results)
    print(f"\n{label} on {n} held-out requests")
    print(f"  valid first try: {first}/{n} ({100 * first / n:.0f}%)")
    print(f"  valid within 3:  {final}/{n} ({100 * final / n:.0f}%)")
    print(f"  latency median {statistics.median(lat):.1f}s, p90 {lat[max(0, int(n * .9) - 1)]:.1f}s")
    common = Counter(e[:90] for r in results for e in r["errors"]).most_common(8)
    if common:
        print("  most common errors:")
        for err, count in common:
            print(f"    {count:3d}x {err}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
