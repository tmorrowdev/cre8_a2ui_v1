"""Function RPC: agent functions (renderer -> agent) and renderer functions (agent -> renderer)."""

from __future__ import annotations

import asyncio
import json
from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

from a2ui_apps.demo_llm import DemoLLM
from a2ui_apps.engine import Engine
from a2ui_apps.llm import ScriptedLLM
from a2ui_apps.rpc import RpcHub
from a2ui_apps.server import create_app
from a2ui_apps.validate import load_catalog


def lines(response) -> list[dict]:
    return [json.loads(line) for line in response.text.splitlines() if line]


def call_agent(client: TestClient, name: str, args: dict, call_id: str = "c1") -> dict:
    message = {
        "version": "1.0",
        "callAgentFunction": {
            "functionCallId": call_id,
            "surfaceId": "s",
            "callFunction": {"@call": name, "catalogId": load_catalog().catalog_id, "args": args},
        },
    }
    res = client.post("/api/rpc", json=message)
    assert res.status_code == 200, res.text
    return lines(res)[0]


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app(DemoLLM()))


def test_agent_function_answers_over_rpc(client):
    in_ten_days = (date.today() + timedelta(days=10)).isoformat()
    reply = call_agent(client, "daysUntil", {"date": in_ten_days})
    assert reply["agentFunctionResponse"]["functionCallId"] == "c1"
    assert reply["agentFunctionResponse"]["value"] in (9, 10, 11)  # UTC vs local date boundary
    assert call_agent(client, "wordCount", {"text": "three short words"})["agentFunctionResponse"]["value"] == 3


def test_unknown_agent_function_is_an_error_reply_not_a_crash(client):
    reply = call_agent(client, "dropTables", {})
    assert reply["agentFunctionResponse"]["error"]["code"] in ("UNKNOWN_FUNCTION", "INVALID_FUNCTION_CALL")


def test_renderer_function_round_trip():
    async def scenario():
        hub = RpcHub(timeout=1.0)
        message, future = hub.ask("getViewport")
        call = message["callRendererFunction"]
        assert call["callFunction"]["@call"] == "getViewport"
        await hub.handle({
            "version": "1.0",
            "rendererFunctionResponse": {"functionCallId": call["functionCallId"], "value": {"width": 390, "height": 844}},
        })
        return await hub.gather([("getViewport", future)])

    assert asyncio.run(scenario()) == {"getViewport": {"width": 390, "height": 844}}


def test_unanswered_renderer_function_times_out_gracefully():
    async def scenario():
        hub = RpcHub(timeout=0.05)
        _, future = hub.ask("getPreferences")
        return await hub.gather([("getPreferences", future)])

    assert asyncio.run(scenario()) == {}


def test_renderer_only_rules_are_enforced():
    hub = RpcHub()
    with pytest.raises(Exception):
        hub.ask("daysUntil")  # an agent function: the agent cannot ask the renderer to run it


def test_narrow_viewport_makes_dashboard_two_up():
    eng = Engine(DemoLLM())
    def grid_variant(context):
        events = list(eng.stream("sales dashboard", context=context))
        comps = [c for e in events if "a2ui" in e for c in e["a2ui"].get("createSurface", {}).get("components", [])]
        return next(c["variant"] for c in comps if c["component"] == "Cre8Grid"), events
    wide, _ = grid_variant({"getViewport": {"width": 1280, "height": 800}})
    narrow, events = grid_variant({"getViewport": {"width": 390, "height": 844}})
    assert (wide, narrow) == ("4up", "2up")
    assert events[0]["step"]["name"] == "context" and "390x844" in events[0]["step"]["detail"]


def test_freeform_tells_the_model_about_the_viewer():
    from test_freeform import ROUTE_FREEFORM, SELECT, VALID

    llm = ScriptedLLM({"route": [ROUTE_FREEFORM], "freeform.select": [SELECT], "freeform.generate": [VALID]})
    list(Engine(llm).stream("a card", context={"getViewport": {"width": 390, "height": 844}, "getPreferences": {"colorScheme": "dark"}}))
    user = next(c for c in llm.calls if c["task"] == "freeform.generate")["messages"][0]["content"]
    assert "Viewer: viewport 390x844px, colorScheme dark" in user
