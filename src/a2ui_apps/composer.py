"""A small fine-tuned composer for the freeform pathway, with the big model behind it.

The freeform pathway's first attempt is the high-volume, schema-bound call:
write Express against a pruned catalog. A distilled model can make that call
fast and cheaply. Everything that needs judgment stays on the planner:

    route / select / form / dashboard / theme ... planner (structured calls)
    freeform.generate, first attempt ............ composer, with the slim prompt
    freeform.generate, repair rounds ............ planner, full prompt + the error
    edits, non-Express formats .................. planner
    composer unreachable (cold, down, no credit)  planner, before anything streams

Validation does not change: the pathway still checks every message against the
full pruned catalog, so the composer can only save time, never let a bad
payload through.

The composer is trained on `slim_system(...)` prompts (scripts/distill.py), so
the slim prompt is the contract between training and serving: change it and
re-distill.
"""

from __future__ import annotations

import logging
import os
from collections import Counter
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

from a2ui_apps.llm import LLM, AnthropicLLM, LLMRefusal, OpenAICompatLLM
from a2ui_apps.pathways.freeform import ComponentSelection

log = logging.getLogger(__name__)

EXPRESS_CONTRACT = "# A2UI Express DSL Output Contract"
SIGNATURES = "## Positional Component Signatures"
EXAMPLES = "\n### Examples:"
EDITING = "You are editing an app"
COMPOSE_TASK = "freeform.generate"


def slim_snippet(snippet: str) -> str:
    """The SDK's Express prompt without per-argument docs or few-shot examples.

    Kept: the grammar, system functions, one positional signature line per
    component (argument order is the whole contract in positional Express),
    function signatures and catalog instructions. Dropped: indented argument
    descriptions and enum lists, and the examples. The composer learned those.
    """
    snippet = snippet.split(EXAMPLES, 1)[0].rstrip()
    out: list[str] = []
    in_signatures = False
    for line in snippet.splitlines():
        if line.startswith("## "):
            in_signatures = line.startswith(SIGNATURES)
        if in_signatures and line.startswith("  "):
            continue
        out.append(line)
    return "\n".join(out)


def is_express(system: list[str]) -> bool:
    return bool(system) and system[0].lstrip().startswith(EXPRESS_CONTRACT)


def slim_system(system: list[str]) -> list[str]:
    """What the composer sees in place of the full system prompt."""
    if not is_express(system):
        return list(system)
    return [slim_snippet(system[0]), *system[1:]]


@dataclass
class RoutedLLM:
    """Implements LLM. Sends first-attempt freeform composes to `composer`, the rest to `planner`."""

    planner: LLM
    composer: LLM
    escalate_repairs: bool = True   # repair rounds go to the planner with the full prompt
    compose_edits: bool = False     # canvas edits stay on the planner until the composer is trained on them
    stats: Counter = field(default_factory=Counter)

    def wants_composer(self, task: str, system: list[str], messages: list[dict[str, Any]]) -> bool:
        if task != COMPOSE_TASK or not is_express(system):
            return False
        if not self.compose_edits and any(EDITING in block for block in system):
            return False
        return not (self.escalate_repairs and len(messages) > 1)

    def structured(self, *, task, system, prompt, schema, effort="medium"):
        self.stats["planner"] += 1
        return self.planner.structured(task=task, system=system, prompt=prompt, schema=schema, effort=effort)

    def text(self, *, task, system, messages, effort="medium"):
        if self.wants_composer(task, system, messages):
            try:
                reply = self.composer.text(task=task, system=slim_system(system), messages=messages, effort=effort)
                self.stats["composer"] += 1
                return reply
            except LLMRefusal:
                raise
            except Exception as e:  # unreachable, cold-start timeout, out of credit, truncated
                self._fell_back(e)
        self.stats["planner"] += 1
        return self.planner.text(task=task, system=system, messages=messages, effort=effort)

    def stream_text(self, *, task, system, messages, effort="medium") -> Iterator[str]:
        if self.wants_composer(task, system, messages):
            stream = self.composer.stream_text(task=task, system=slim_system(system), messages=messages, effort=effort)
            try:
                first = next(stream)
            except StopIteration:
                # Empty reply: the pathway reports NO_UI and the repair goes to the planner.
                self.stats["composer"] += 1
                return
            except LLMRefusal:
                raise
            except Exception as e:  # nothing was streamed yet, so the planner can take over cleanly
                self._fell_back(e)
            else:
                self.stats["composer"] += 1
                yield first
                yield from stream  # a mid-stream failure surfaces like any other model error
                return
        self.stats["planner"] += 1
        yield from self.planner.stream_text(task=task, system=system, messages=messages, effort=effort)

    def _fell_back(self, error: Exception) -> None:
        self.stats["fallback"] += 1
        log.warning("composer unavailable, using planner: %s: %s", type(error).__name__, error)


@dataclass
class RecordingLLM:
    """Implements LLM. Passes every call through to `inner` and records it (scripts/distill.py)."""

    inner: LLM
    calls: list[dict[str, Any]] = field(default_factory=list)

    def structured(self, *, task, system, prompt, schema, effort="medium"):
        result = self.inner.structured(task=task, system=system, prompt=prompt, schema=schema, effort=effort)
        self.calls.append({"task": task, "system": list(system), "prompt": prompt, "result": result.model_dump()})
        return result

    def text(self, *, task, system, messages, effort="medium"):
        reply = self.inner.text(task=task, system=system, messages=messages, effort=effort)
        self.calls.append({"task": task, "system": list(system), "messages": [dict(m) for m in messages], "reply": reply})
        return reply

    def stream_text(self, *, task, system, messages, effort="medium"):
        snapshot = {"task": task, "system": list(system), "messages": [dict(m) for m in messages]}
        reply = ""
        for chunk in self.inner.stream_text(task=task, system=system, messages=messages, effort=effort):
            reply += chunk
            yield chunk
        self.calls.append({**snapshot, "reply": reply})

    def last(self, task: str) -> dict[str, Any] | None:
        return next((c for c in reversed(self.calls) if c["task"] == task), None)


@dataclass
class ReplaySelection:
    """Planner stand-in for evals and smoke tests: answers freeform.select with a fixed
    component choice and sends any text call to `inner` (none: composer-only runs)."""

    components: list[str]
    inner: LLM | None = None

    def structured(self, *, task, system, prompt, schema, effort="medium"):
        if schema is not ComponentSelection:
            raise AssertionError(f"unexpected planner call {task}")
        return ComponentSelection(components=self.components)

    def _inner(self) -> LLM:
        if self.inner is None:  # RoutedLLM only lands here when the composer could not be reached
            raise RuntimeError("composer unreachable (the eval does not fall back to a planner)")
        return self.inner

    def text(self, **kw):
        return self._inner().text(**kw)

    def stream_text(self, **kw):
        yield from self._inner().stream_text(**kw)


def openai_from_env(prefix: str) -> OpenAICompatLLM | None:
    """`{prefix}_URL`, `{prefix}_MODEL`, `{prefix}_KEY`, `{prefix}_MAX_TOKENS` -> a client, or None if no URL."""
    url = os.environ.get(f"{prefix}_URL")
    if not url:
        return None
    return OpenAICompatLLM(
        base_url=url,
        model=os.environ.get(f"{prefix}_MODEL", "a2ui-composer"),
        api_key=os.environ.get(f"{prefix}_KEY"),
        max_tokens=int(os.environ.get(f"{prefix}_MAX_TOKENS", "16000")),
    )


def llm_from_env() -> LLM:
    """The server's model stack.

    Planner: Claude (default) or any OpenAI-compatible endpoint via A2UI_APPS_PLANNER_URL
             (e.g. Kimi on Ollama Cloud: https://ollama.com/v1).
    Composer: optional, via A2UI_APPS_COMPOSER_URL (the fine-tuned model on Modal or Ollama).
    """
    if os.environ.get("A2UI_APPS_FAKE_LLM"):
        from a2ui_apps.demo_llm import DemoLLM

        return DemoLLM()
    planner: LLM = openai_from_env("A2UI_APPS_PLANNER") or AnthropicLLM()
    composer = openai_from_env("A2UI_APPS_COMPOSER")
    if composer is None:
        return planner
    if "A2UI_APPS_COMPOSER_MAX_TOKENS" not in os.environ:
        composer.max_tokens = 4096  # the composer serves a 16k context; the slim prompt plus this fits
    return RoutedLLM(planner=planner, composer=composer)
