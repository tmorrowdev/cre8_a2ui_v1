from __future__ import annotations

import pytest

from a2ui_apps.engine import Engine
from a2ui_apps.llm import ScriptedLLM
from a2ui_apps.pathways.dashboard import DashboardPathway, DashboardSlots
from a2ui_apps.pathways.form import FormPathway, FormSlots, normalize
from a2ui_apps.validate import validate_messages
from conftest import errors_of

CONTACT = {
    "title": "Contact us",
    "intro": "Send us a note and we will reply within a day.",
    "fields": [
        {"name": "full_name", "label": "Full name", "kind": "text", "required": True},
        {"name": "email", "label": "Email", "kind": "email", "required": True},
        {"name": "topic", "label": "Topic", "kind": "select", "options": ["Sales", "Support", "Sales"]},
        {"name": "message", "label": "Message", "kind": "text"},
    ],
    "submit_label": "Send",
    "success_message": "Thanks, we got it.",
}

DASHBOARD = {
    "title": "Store overview",
    "subtitle": "Sample data for the last 30 days.",
    "metrics": [
        {"label": "Revenue", "value": "$48.2k", "delta": "+6.1%", "trend": "up"},
        {"label": "Refunds", "value": "1.9%", "delta": "+0.4%", "trend": "up", "good_when_up": False},
        {"label": "Orders", "value": "1,204", "trend": "flat"},
    ],
    "sections": [
        {"title": "Top products", "kind": "table", "columns": ["Product", "Units"], "rows": [["Mug", "320"], ["Tee"]]},
        {"title": "Goals", "kind": "progress", "items": [{"label": "Q4 revenue", "value": 62, "max": 100}]},
    ],
}


def assert_valid(messages, envelope_validator):
    for m in messages:
        assert errors_of(envelope_validator, m) == [], m
    assert validate_messages(messages) == []


# ─── Routing ─────────────────────────────────────────────────────────────────


def test_rules_route_without_calling_the_model(envelope_validator):
    llm = ScriptedLLM({"form.plan": [CONTACT]})
    gen = Engine(llm).generate("Build a contact form for my bakery")
    assert gen.pathway == "form"
    assert [c["task"] for c in llm.calls] == ["form.plan"]
    assert gen.trace[0].deterministic and "rules" in gen.trace[0].detail
    assert_valid(gen.messages, envelope_validator)


def test_contact_button_does_not_make_a_form():
    from a2ui_apps.engine import default_pathways
    from a2ui_apps.router import keyword_matches

    matches = keyword_matches("A team member directory with roles and a contact button for each person", default_pathways())
    assert "form" not in matches
    assert "form" in keyword_matches("Build a contact form for my bakery", default_pathways())


def test_stats_on_a_pricing_page_do_not_make_a_dashboard():
    from a2ui_apps.engine import default_pathways
    from a2ui_apps.router import keyword_matches

    matches = keyword_matches("A pricing page with three plans and headline usage stats above them", default_pathways())
    assert "dashboard" not in matches
    assert "dashboard" in keyword_matches("A KPI dashboard for support", default_pathways())


def test_ambiguous_prompt_asks_the_model():
    llm = ScriptedLLM(
        {
            "route": [{"pathway": "dashboard", "confidence": 0.8, "reason": "metrics"}],
            "dashboard.plan": [DASHBOARD],
        }
    )
    gen = Engine(llm).generate("A sign up form analytics dashboard")  # matches form and dashboard
    assert gen.pathway == "dashboard"
    assert [c["task"] for c in llm.calls] == ["route", "dashboard.plan"]
    assert not gen.trace[0].deterministic


# ─── Form ────────────────────────────────────────────────────────────────────


def test_normalize_dedupes_and_sanitizes_names():
    slots = normalize(
        FormSlots.model_validate(
            {
                **CONTACT,
                "fields": [
                    {"name": "E-mail address", "label": "Email"},
                    {"name": "e_mail_address", "label": "Email again"},
                    {"name": "9lives", "label": "Lives"},
                    {"name": "", "label": "Café ☕"},
                    {"name": "pick", "label": "Pick", "kind": "select", "options": []},
                ],
            }
        )
    )
    names = [f.name for f in slots.fields]
    assert names == ["e_mail_address", "e_mail_address_2", "field_9lives", "caf", "pick"]
    assert slots.fields[-1].kind == "text"  # select without options degrades


@pytest.mark.parametrize(
    "fields",
    [
        CONTACT["fields"],
        [{"name": "ünïcode", "label": "Ünïcode ✓", "kind": "date", "required": True}],
        [{"name": f"f{i}", "label": f"Field {i}"} for i in range(20)],  # capped at 12
        [],  # degrades to a single message field
    ],
)
def test_form_assembly_is_always_valid(fields, envelope_validator):
    pathway = FormPathway()
    slots = normalize(FormSlots.model_validate({**CONTACT, "fields": fields}))
    assert_valid(pathway.assemble(slots, "s"), envelope_validator)


def test_submit_with_errors_then_success(envelope_validator):
    engine = Engine(ScriptedLLM({"form.plan": [CONTACT]}))
    gen = engine.generate("contact form")
    sid = gen.surface_id

    bad = engine.handle_action(
        {"version": "1.0", "action": {"name": "submit", "surfaceId": sid, "context": {"full_name": "", "email": "nope"}}}
    )
    comps = {c["id"]: c for c in bad[0]["updateComponents"]["components"]}
    assert comps["status"]["status"] == "error"
    assert comps["field_full_name"]["isError"] and comps["field_email"]["errorNote"] == "Enter a valid email address."
    assert all(errors_of(envelope_validator, m) == [] for m in bad)

    good = engine.handle_action(
        {"version": "1.0", "action": {"name": "submit", "surfaceId": sid, "context": {"full_name": "Ada", "email": "ada@x.io"}}}
    )
    comps = {c["id"]: c for c in good[0]["updateComponents"]["components"]}
    assert comps["status"]["status"] == "success"
    assert comps["field_email"]["isError"] is False and comps["field_email"]["errorNote"] == ""
    assert good[1]["updateDataModel"]["path"] == "/submitted"
    assert engine.surfaces[sid].state.data_model(sid)["submitted"]["full_name"] == "Ada"


def test_action_for_unknown_surface_raises():
    with pytest.raises(KeyError):
        Engine(ScriptedLLM()).handle_action({"action": {"name": "submit", "surfaceId": "nope"}})


# ─── Dashboard ───────────────────────────────────────────────────────────────


@pytest.mark.parametrize("n_metrics", [0, 1, 2, 3, 4, 7, 12])
def test_dashboard_assembly_is_always_valid(n_metrics, envelope_validator):
    metrics = [{"label": f"M{i}", "value": str(i), "delta": "+1", "trend": "up"} for i in range(n_metrics)]
    pathway = DashboardPathway()
    slots = pathway.plan("x", ScriptedLLM({"dashboard.plan": [{**DASHBOARD, "metrics": metrics}]}))
    assert_valid(pathway.assemble(slots, "s"), envelope_validator)


def test_dashboard_pads_ragged_rows_and_colors_deltas():
    pathway = DashboardPathway()
    slots = pathway.plan("x", ScriptedLLM({"dashboard.plan": [DASHBOARD]}))
    assert slots.sections[0].rows[1] == ["Tee", ""]
    comps = pathway.assemble(slots, "s")[0]["createSurface"]["components"]
    badges = [c["status"] for c in comps if c["component"] == "Cre8Badge"]
    assert badges == ["success", "error"]


def test_dashboard_drops_empty_sections():
    pathway = DashboardPathway()
    slots = pathway.plan(
        "x",
        ScriptedLLM({"dashboard.plan": [{**DASHBOARD, "sections": [{"title": "Empty", "kind": "table", "columns": ["A"]}]}]}),
    )
    assert slots.sections == []
