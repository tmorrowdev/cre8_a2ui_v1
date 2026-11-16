"""The model boundary. Pathways ask for two things only: a typed object, or text.

Keeping the surface this small is what makes the pathways semi-deterministic:
everything the model returns is either validated by pydantic (structured) or by
a2ui_core (freeform JSON), and tests swap in `ScriptedLLM` with no API key.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from collections.abc import Iterator
from typing import Any, Callable, Literal, Protocol, TypeVar

import anthropic
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)
Effort = Literal["low", "medium", "high", "xhigh", "max"]

DEFAULT_MODEL = os.environ.get("A2UI_APPS_MODEL", "claude-opus-5-5")
FALLBACK_BETA = "server-side-fallback-2026-07-01"


class LLMRefusal(RuntimeError):
    """The model (and its fallback chain) declined the request."""


class LLMIncomplete(RuntimeError):
    """The response stopped before producing a usable answer (e.g. max_tokens)."""


class LLM(Protocol):
    def structured(
        self, *, task: str, system: list[str], prompt: str, schema: type[T], effort: Effort = "medium"
    ) -> T: ...

    def text(
        self, *, task: str, system: list[str], messages: list[dict[str, Any]], effort: Effort = "medium"
    ) -> str: ...

    def stream_text(
        self, *, task: str, system: list[str], messages: list[dict[str, Any]], effort: Effort = "medium"
    ) -> Iterator[str]: ...


def _system_blocks(system: list[str]) -> list[dict[str, Any]]:
    """Static text first; the breakpoint on the last block caches the whole prefix."""
    blocks: list[dict[str, Any]] = [{"type": "text", "text": text} for text in system]
    if blocks:
        blocks[-1]["cache_control"] = {"type": "ephemeral"}
    return blocks


@dataclass
class AnthropicLLM:
    """Claude through the official SDK.

    Server-side refusal fallbacks are on (`fallbacks="default"`), so a policy
    decline is retried on a fallback model inside the same call; a refusal that
    survives the chain raises LLMRefusal.
    """

    model: str = DEFAULT_MODEL
    client: anthropic.Anthropic = field(default_factory=anthropic.Anthropic)
    max_tokens: int = 16000
    stream_max_tokens: int = 64000

    def _check(self, response: Any) -> None:
        if response.stop_reason == "refusal":
            details = getattr(response, "stop_details", None)
            raise LLMRefusal(getattr(details, "explanation", None) or "request declined")
        if response.stop_reason == "max_tokens":
            raise LLMIncomplete("response hit max_tokens")

    def structured(self, *, task, system, prompt, schema, effort="medium"):
        response = self.client.beta.messages.parse(
            model=self.model,
            max_tokens=self.max_tokens,
            betas=[FALLBACK_BETA],
            fallbacks="default",
            system=_system_blocks(system),
            messages=[{"role": "user", "content": prompt}],
            output_config={"effort": effort},
            output_format=schema,
        )
        self._check(response)
        if response.parsed_output is None:
            raise LLMIncomplete(f"{task}: no structured output returned")
        return response.parsed_output

    def text(self, *, task, system, messages, effort="medium"):
        response = self.client.beta.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            betas=[FALLBACK_BETA],
            fallbacks="default",
            system=_system_blocks(system),
            messages=messages,
            output_config={"effort": effort},
        )
        self._check(response)
        return "".join(block.text for block in response.content if block.type == "text")

    def stream_text(self, *, task, system, messages, effort="medium"):
        """Text deltas as they arrive; refusal/truncation raise after the stream ends."""
        with self.client.beta.messages.stream(
            model=self.model,
            max_tokens=self.stream_max_tokens,
            betas=[FALLBACK_BETA],
            fallbacks="default",
            system=_system_blocks(system),
            messages=messages,
            output_config={"effort": effort},
        ) as stream:
            yield from stream.text_stream
            self._check(stream.get_final_message())


Responder = Callable[[dict[str, Any]], Any]


@dataclass
class ScriptedLLM:
    """A deterministic stand-in: each task maps to a queue of responses.

    A response is a value, or a callable receiving the call's kwargs. Every call
    is recorded in `calls`, so tests can assert what the model was (not) asked.
    """

    script: dict[str, list[Any]] = field(default_factory=dict)
    calls: list[dict[str, Any]] = field(default_factory=list)

    def _next(self, task: str, call: dict[str, Any]) -> Any:
        self.calls.append(call)
        queue = self.script.get(task)
        if not queue:
            raise AssertionError(f"ScriptedLLM: no response scripted for task {task!r}")
        item = queue.pop(0)
        return item(call) if callable(item) else item

    def structured(self, *, task, system, prompt, schema, effort="medium"):
        value = self._next(task, {"task": task, "prompt": prompt, "schema": schema, "effort": effort})
        return value if isinstance(value, schema) else schema.model_validate(value)

    def text(self, *, task, system, messages, effort="medium"):
        # Snapshot: callers keep appending to the same list after the call.
        return self._next(task, {"task": task, "system": list(system), "messages": [dict(m) for m in messages], "effort": effort})

    def stream_text(self, *, task, system, messages, effort="medium", chunk: int = 23):
        """The scripted text, in small chunks, so tests exercise incremental parsing."""
        text = self.text(task=task, system=system, messages=messages, effort=effort)
        for i in range(0, len(text), chunk):
            yield text[i : i + chunk]
