"""The fine-tuned composer path: slim prompt, routing, fallback, and the OpenAI-compatible client."""

from __future__ import annotations

import json

import httpx
import pytest
from pydantic import BaseModel

from a2ui_apps.composer import RecordingLLM, RoutedLLM, llm_from_env, slim_system
from a2ui_apps.engine import Engine
from a2ui_apps.llm import AnthropicLLM, LLMIncomplete, OpenAICompatLLM, ScriptedLLM
from test_freeform import INVALID_ENUM, ROUTE_FREEFORM, SELECT, VALID


def full_freeform_system() -> list[str]:
    """The real system prompt the freeform pathway sends, captured through a recorder."""
    rec = RecordingLLM(ScriptedLLM({"route": [ROUTE_FREEFORM], "freeform.select": [SELECT], "freeform.generate": [VALID]}))
    list(Engine(rec).stream("a little card"))
    return rec.last("freeform.generate")["system"]


def routed(composer_replies, planner_replies):
    planner = ScriptedLLM({"route": [ROUTE_FREEFORM], "freeform.select": [SELECT], "freeform.generate": list(planner_replies)})
    composer = ScriptedLLM({"freeform.generate": list(composer_replies)})
    return RoutedLLM(planner=planner, composer=composer), planner, composer


# ---- slim prompt -------------------------------------------------------------

def test_slim_prompt_keeps_signatures_and_rules_drops_docs_and_examples():
    full = full_freeform_system()
    slim = slim_system(full)
    assert slim[0].startswith("# A2UI Express DSL Output Contract")
    for kept in ("## Grammar Rules", "• Cre8Card(", "• Cre8Badge(", "• HtmlDiv(", "## Catalog Instructions"):
        assert kept in slim[0], kept
    assert "### Examples:" in full[0] and "### Examples:" not in slim[0]
    def signatures(text: str) -> str:
        return text.split("## Positional Component Signatures", 1)[1].split("\n## ", 1)[0]

    assert "  - Description:" in signatures(full[0]) and "  - Description:" not in signatures(slim[0])
    assert slim[1:] == full[1:], "the app guide is unchanged"
    assert len(slim[0]) < len(full[0]) / 2


def test_slim_leaves_other_prompts_alone():
    assert slim_system(["Pick components.", "x"]) == ["Pick components.", "x"]


# ---- routing -----------------------------------------------------------------

def test_first_attempt_goes_to_composer_with_slim_prompt():
    llm, planner, composer = routed([VALID], [])
    events = list(Engine(llm).stream("a little card"))
    assert any("a2ui" in e for e in events)
    call = composer.calls[0]
    assert "### Examples:" not in call["system"][0]
    assert not [c for c in planner.calls if c["task"] == "freeform.generate"]
    assert llm.stats["composer"] == 1


def test_repair_escalates_to_planner_with_full_prompt():
    llm, planner, composer = routed([INVALID_ENUM], [VALID])
    events = list(Engine(llm).stream("a little card"))
    assert events[-1]["trace"]["pathway"] == "freeform"
    repair = next(c for c in planner.calls if c["task"] == "freeform.generate")
    assert "### Examples:" in repair["system"][0], "the planner gets the full prompt"
    assert "'huge' is not a valid enum choice" in repair["messages"][-1]["content"]
    assert llm.stats["composer"] == 1


class Down:
    """A composer whose endpoint is unreachable."""

    def stream_text(self, **kw):
        raise httpx.ConnectError("connection refused")
        yield  # pragma: no cover

    def text(self, **kw):
        raise httpx.ConnectError("connection refused")


def test_unreachable_composer_falls_back_before_streaming():
    planner = ScriptedLLM({"route": [ROUTE_FREEFORM], "freeform.select": [SELECT], "freeform.generate": [VALID]})
    llm = RoutedLLM(planner=planner, composer=Down())
    events = list(Engine(llm).stream("a little card"))
    assert not [e for e in events if e.get("step", {}).get("name") == "repair"]
    assert llm.stats["fallback"] == 1


def test_edits_and_other_tasks_stay_on_planner():
    llm = RoutedLLM(planner=ScriptedLLM(), composer=ScriptedLLM())
    express = full_freeform_system()
    one = [{"role": "user", "content": "x"}]
    assert llm.wants_composer("freeform.generate", express, one)
    assert not llm.wants_composer("freeform.generate", [express[0], "You are editing an app the user already sees."], one)
    assert not llm.wants_composer("freeform.generate", ["# Direct JSON contract"], one)
    assert not llm.wants_composer("author.write", express, one)
    assert not llm.wants_composer("freeform.generate", express, one * 3)


def test_recording_captures_streamed_reply():
    rec = RecordingLLM(ScriptedLLM({"freeform.generate": ["hello world"]}))
    assert "".join(rec.stream_text(task="freeform.generate", system=["s"], messages=[{"role": "user", "content": "u"}])) == "hello world"
    assert rec.last("freeform.generate")["reply"] == "hello world"


# ---- OpenAI-compatible client -------------------------------------------------

class Pick(BaseModel):
    components: list[str]


def client(handler) -> OpenAICompatLLM:
    return OpenAICompatLLM(base_url="http://test/v1", model="m", api_key="k", transport=httpx.MockTransport(handler))


def completion(content: str, finish: str = "stop") -> httpx.Response:
    return httpx.Response(200, json={"choices": [{"message": {"content": content}, "finish_reason": finish}]})


def test_openai_text_sends_system_auth_and_model():
    seen = {}

    def handler(request):
        seen["body"] = json.loads(request.content)
        seen["auth"] = request.headers["authorization"]
        return completion("hi")

    assert client(handler).text(task="t", system=["a", "b"], messages=[{"role": "user", "content": "u"}]) == "hi"
    assert seen["auth"] == "Bearer k"
    assert seen["body"]["model"] == "m"
    assert seen["body"]["messages"][0] == {"role": "system", "content": "a\n\nb"}


def test_openai_stream_parses_sse():
    sse = "".join(
        f"data: {json.dumps({'choices': [{'delta': {'content': c}, 'finish_reason': None}]})}\n\n" for c in ["<a2", "ui>", "!"]
    ) + "data: [DONE]\n\n"
    llm = client(lambda r: httpx.Response(200, text=sse, headers={"content-type": "text/event-stream"}))
    assert list(llm.stream_text(task="t", system=[], messages=[])) == ["<a2", "ui>", "!"]


def test_openai_stream_raises_on_truncation():
    sse = f"data: {json.dumps({'choices': [{'delta': {'content': 'x'}, 'finish_reason': 'length'}]})}\n\ndata: [DONE]\n\n"
    llm = client(lambda r: httpx.Response(200, text=sse))
    with pytest.raises(LLMIncomplete):
        list(llm.stream_text(task="t", system=[], messages=[]))


def test_openai_structured_validates_and_repairs_once():
    replies = iter(['{"components": "oops"}', '```json\n{"components": ["Cre8Card"]}\n```'])
    bodies = []

    def handler(request):
        bodies.append(json.loads(request.content))
        return completion(next(replies))

    out = client(handler).structured(task="t", system=["pick"], prompt="p", schema=Pick)
    assert out == Pick(components=["Cre8Card"])
    assert bodies[0]["response_format"]["type"] == "json_schema"
    assert "Invalid" in bodies[1]["messages"][-1]["content"]


# ---- wiring ------------------------------------------------------------------

def test_llm_from_env(monkeypatch):
    for k in ("A2UI_APPS_FAKE_LLM", "A2UI_APPS_PLANNER_URL", "A2UI_APPS_COMPOSER_URL", "A2UI_APPS_COMPOSER_MAX_TOKENS"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test")
    assert isinstance(llm_from_env(), AnthropicLLM)

    monkeypatch.setenv("A2UI_APPS_COMPOSER_URL", "https://x.modal.run/v1")
    llm = llm_from_env()
    assert isinstance(llm, RoutedLLM) and isinstance(llm.planner, AnthropicLLM)
    assert llm.composer.model == "a2ui-composer" and llm.composer.max_tokens == 4096

    monkeypatch.setenv("A2UI_APPS_PLANNER_URL", "https://ollama.com/v1")
    monkeypatch.setenv("A2UI_APPS_PLANNER_MODEL", "kimi-k2.6")
    assert llm_from_env().planner.model == "kimi-k2.6"
