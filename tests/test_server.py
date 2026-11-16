from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient

from a2ui_apps.demo_llm import DemoLLM
from a2ui_apps.server import create_app
from conftest import errors_of


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app(DemoLLM()))


def lines(response) -> list[dict]:
    return [json.loads(line) for line in response.text.splitlines() if line]


@pytest.mark.parametrize("prompt, pathway", [("a signup form", "form"), ("sales dashboard", "dashboard"), ("a haiku", "freeform")])
def test_generate_streams_events_then_trace(client, envelope_validator, prompt, pathway):
    res = client.post("/api/generate", json={"prompt": prompt})
    assert res.status_code == 200 and res.headers["content-type"].startswith("application/jsonl")
    events = lines(res)
    assert not [e for e in events if "error" in e], events
    trace = events[-1]["trace"]
    assert trace["pathway"] == pathway
    assert trace["steps"][0]["name"] == "route" and trace["steps"][-1]["name"] == "validate"
    messages = [e["a2ui"] for e in events if "a2ui" in e]
    assert messages and "createSurface" in messages[0]
    for m in messages:
        assert errors_of(envelope_validator, m) == []


def test_unknown_format_is_rejected(client):
    assert client.post("/api/generate", json={"prompt": "x", "format": "yaml"}).status_code == 400


def test_action_round_trip_uses_posted_data_model(client):
    events = lines(client.post("/api/generate", json={"prompt": "a signup form"}))
    sid = events[-1]["trace"]["surfaceId"]
    action = {"version": "1.0", "action": {"name": "submit", "surfaceId": sid, "sourceComponentId": "submit", "context": {}}}
    data = {"form": {"full_name": "Ada", "email": "ada@example.com", "plan": "Team", "notes": ""}}
    res = client.post("/api/action", json={"message": action, "dataModel": data})
    assert res.status_code == 200
    out = lines(res)
    status = next(c for c in out[0]["updateComponents"]["components"] if c["id"] == "status")
    assert status["status"] == "success"


def test_action_errors(client):
    assert client.post("/api/action", json={"message": {"nope": 1}}).status_code == 400
    missing = {"version": "1.0", "action": {"name": "submit", "surfaceId": "ghost"}}
    assert client.post("/api/action", json={"message": missing}).status_code == 404


def test_catalog_endpoint(client):
    doc = client.get("/api/catalog").json()
    assert doc["catalogId"].endswith("/cre8-wc/3.0.1")
