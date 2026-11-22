"""The model boundary. Pathways ask for two things only: a typed object, or text.

Keeping the surface this small is what makes the pathways semi-deterministic:
everything the model returns is either validated by pydantic (structured) or by
a2ui_core (freeform JSON), and tests swap in `ScriptedLLM` with no API key.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from collections.abc import Iterator
from typing import Any, Callable, Literal, Protocol, TypeVar

import anthropic
import httpx
from pydantic import BaseModel, ValidationError

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


@dataclass
class OpenAICompatLLM:
    """Any OpenAI-compatible chat endpoint: vLLM on Modal, a LiteLLM proxy, Ollama Cloud.

    Plain httpx, so no extra dependency. `effort` has no portable equivalent and
    is ignored. Structured output asks for a JSON schema (vLLM and Ollama enforce
    it) and is still validated with pydantic, with one repair round, because not
    every server enforces the schema.
    """

    base_url: str
    model: str
    api_key: str | None = None
    max_tokens: int = 16000
    temperature: float = 0.2
    timeout: float = 300.0
    transport: httpx.BaseTransport | None = None  # tests inject httpx.MockTransport
    _http: httpx.Client | None = field(default=None, init=False, repr=False)

    @property
    def http(self) -> httpx.Client:
        if self._http is None:
            headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
            self._http = httpx.Client(
                base_url=self.base_url.rstrip("/"), headers=headers, timeout=self.timeout, transport=self.transport
            )
        return self._http

    def _body(self, system: list[str], messages: list[dict[str, Any]], **extra: Any) -> dict[str, Any]:
        chat = ([{"role": "system", "content": "\n\n".join(system)}] if system else []) + list(messages)
        return {"model": self.model, "messages": chat, "max_tokens": self.max_tokens, "temperature": self.temperature, **extra}

    def _complete(self, body: dict[str, Any]) -> str:
        response = self.http.post("/chat/completions", json=body)
        response.raise_for_status()
        choice = response.json()["choices"][0]
        if choice.get("finish_reason") == "length":
            raise LLMIncomplete("response hit max_tokens")
        return choice["message"].get("content") or ""

    def structured(self, *, task, system, prompt, schema, effort="medium"):
        messages: list[dict[str, Any]] = [{"role": "user", "content": prompt}]
        system = [*system, "Respond with one JSON object matching this JSON schema:\n" + json.dumps(schema.model_json_schema())]
        fmt = {"type": "json_schema", "json_schema": {"name": schema.__name__, "schema": schema.model_json_schema()}}
        error: Exception | None = None
        for _ in range(2):
            raw = self._complete(self._body(system, messages, response_format=fmt))
            try:
                return schema.model_validate_json(_strip_fence(raw))
            except ValidationError as e:
                error = e
                messages += [{"role": "assistant", "content": raw}, {"role": "user", "content": f"Invalid: {e}. Return the corrected JSON only."}]
        raise LLMIncomplete(f"{task}: no valid {schema.__name__} ({error})")

    def text(self, *, task, system, messages, effort="medium"):
        return self._complete(self._body(system, messages))

    def stream_text(self, *, task, system, messages, effort="medium"):
        finish = None
        with self.http.stream("POST", "/chat/completions", json=self._body(system, messages, stream=True)) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if not line.startswith("data:"):
                    continue
                data = line[5:].strip()
                if data == "[DONE]":
                    break
                choice = (json.loads(data).get("choices") or [{}])[0]
                if delta := (choice.get("delta") or {}).get("content"):
                    yield delta
                finish = choice.get("finish_reason") or finish
        if finish == "length":
            raise LLMIncomplete("response hit max_tokens")


def _strip_fence(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1].rsplit("```", 1)[0]
    return text


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
