"""The freeform pathway on a2ui-agent-sdk: pruned prompt, streamed Express, repair."""

from __future__ import annotations

import pytest

from a2ui_apps.engine import Engine
from a2ui_apps.llm import ScriptedLLM
from a2ui_apps.pathways.base import PathwayFailed
from a2ui_apps.validate import validate_messages
from conftest import errors_of

ROUTE_FREEFORM = {"pathway": "freeform", "confidence": 0.9, "reason": "custom"}
SELECT = {"components": ["Cre8Card", "Cre8Badge", "NotAComponent"]}

VALID = '''Built a small card.
<a2ui>
root = HtmlDiv(display="flex", direction="column", gap="16", children=[title, card, go])
title = Cre8Heading(type="headline-large", children=[Text(text="Hello there, this streams in")])
card = Cre8Card(slot_default=[Cre8Badge(text="New", status="info")])
$/count = 3
go = Cre8Button(text="Go", variant="primary", on_click=Event("go", {n: $/count}))
</a2ui>'''

INVALID_ENUM = '<a2ui>\nroot = HtmlDiv(children=[b])\nb = Cre8Button(text="x", variant="huge")\n</a2ui>'


def engine(*generate):
    llm = ScriptedLLM({"route": [ROUTE_FREEFORM], "freeform.select": [SELECT], "freeform.generate": list(generate)})
    return Engine(llm), llm


def test_streams_progressively_and_validates(envelope_validator):
    eng, llm = engine(VALID)
    events = list(eng.stream("a little card"))
    a2ui = [e["a2ui"] for e in events if "a2ui" in e]
    assert "createSurface" in a2ui[0] and [c["id"] for c in a2ui[0]["createSurface"]["components"]] == ["root"]
    assert len(a2ui) > 3, "root first, then children as each statement closes"
    assert any("updateDataModel" in m for m in a2ui)
    assert [e["text"].strip() for e in events if "text" in e] == ["Built a small card."]
    for m in a2ui:
        assert errors_of(envelope_validator, m) == []
    trace = events[-1]["trace"]
    sid = trace["surfaceId"]
    snapshot = eng.surfaces[sid].state.snapshot(sid)
    assert validate_messages(snapshot) == [], "the finished surface passes strict validation"


def test_prompt_is_pruned_to_selected_components():
    eng, llm = engine(VALID)
    list(eng.stream("a little card"))
    call = next(c for c in llm.calls if c["task"] == "freeform.generate")
    prompt = "\n".join(call["system"])
    assert call["effort"] == "high"
    for kept in ("Cre8Card(", "Cre8Badge(", "HtmlDiv(", "Cre8Button("):
        assert kept in prompt, kept
    for pruned in ("Cre8Tabs(", "Cre8Chart(", "Cre8Modal(", "NotAComponent"):
        assert pruned not in prompt, pruned
    from a2ui_apps.sdk import make_processor

    full = make_processor(surface_id="s").prompt_snippet
    assert len(prompt) < len(full) / 4, f"pruned {len(prompt)} vs full {len(full)} chars"


def test_repairs_with_sdk_error_and_deletes_partial_surface():
    eng, llm = engine(INVALID_ENUM, VALID)
    events = list(eng.stream("a little card"))
    repair_prompt = [c for c in llm.calls if c["task"] == "freeform.generate"][1]["messages"][-1]["content"]
    assert "'huge' is not a valid enum choice" in repair_prompt
    assert any(e.get("step", {}).get("name") == "repair" for e in events)
    assert "in 2 attempts" in [s["detail"] for s in events[-1]["trace"]["steps"] if s["name"] == "generate"][0]


def test_partial_surface_is_deleted_before_retry():
    # The first attempt streams a valid root before failing, so the browser holds a partial surface.
    partial_then_bad = '<a2ui>\nroot = HtmlDiv(children=[a, b])\na = Cre8Heading(children=[Text(text="ok")])\nb = Cre8Button(text="x", variant="huge")\n</a2ui>'
    eng, _ = engine(partial_then_bad, VALID)
    a2ui = [e["a2ui"] for e in eng.stream("a little card") if "a2ui" in e]
    deletes = [i for i, m in enumerate(a2ui) if "deleteSurface" in m]
    creates = [i for i, m in enumerate(a2ui) if "createSurface" in m]
    assert deletes and len(creates) == 2 and creates[0] < deletes[0] < creates[1]


def test_gives_up_after_max_attempts():
    eng, _ = engine("no ui here", INVALID_ENUM, '<a2ui>\nroot = Row()\n</a2ui>')
    with pytest.raises(PathwayFailed) as exc:
        list(eng.stream("weird thing"))
    assert exc.value.errors


def test_unknown_property_is_rejected():
    eng, llm = engine('<a2ui>\nroot = Cre8Button(text="x", bogus=1)\n</a2ui>', VALID)
    list(eng.stream("a button"))
    repair_prompt = [c for c in llm.calls if c["task"] == "freeform.generate"][1]["messages"][-1]["content"]
    assert "bogus" in repair_prompt


@pytest.mark.parametrize("fmt", ["express", "direct_json"])
def test_format_selection_changes_the_prompt(fmt):
    from a2ui_apps.sdk import make_processor

    p = make_processor(surface_id="s", fmt=fmt, components=["Cre8Button"]).prompt_snippet
    assert ("<a2ui>" in p) == (fmt == "express")
    assert ("<a2ui-json>" in p) == (fmt == "direct_json")


# ─── Canvas mode: editing a live surface ─────────────────────────────────────

EDIT = '''Added a badge and renamed the button.
<a2ui>
surface("{sid}", update=true)
root = HtmlDiv(display="flex", direction="column", gap="16", children=[title, card, badge, go])
badge = Cre8Badge(text="Edited", status="success")
go = Cre8Button(text="Go again", variant="secondary", on_click=Event("go", {{n: $/count}}))
$/count = 4
</a2ui>'''


def built_surface():
    llm = ScriptedLLM({"route": [ROUTE_FREEFORM], "freeform.select": [SELECT, SELECT, SELECT], "freeform.generate": [VALID]})
    eng = Engine(llm)
    sid = list(eng.stream("a little card"))[-1]["trace"]["surfaceId"]
    return eng, llm, sid


def test_edit_streams_updates_and_keeps_untouched_components(envelope_validator):
    eng, llm, sid = built_surface()
    llm.script["freeform.generate"] = [EDIT.format(sid=sid)]
    events = list(eng.stream("add a badge, rename the button", surface_id=sid))
    a2ui = [e["a2ui"] for e in events if "a2ui" in e]
    assert a2ui and all(set(m) - {"version"} <= {"updateComponents", "updateDataModel"} for m in a2ui)
    for m in a2ui:
        assert errors_of(envelope_validator, m) == []
    snap = eng.surfaces[sid].state.snapshot(sid)[0]["createSurface"]
    by_id = {c["id"]: c for c in snap["components"]}
    assert by_id["badge"]["text"] == "Edited" and by_id["go"]["text"] == "Go again"
    assert "title" in by_id and "card" in by_id, "untouched components survive"
    assert snap["dataModel"]["count"] == 4
    assert events[-1]["trace"]["edited"] is True
    call = [c for c in llm.calls if c["task"] == "freeform.generate"][-1]
    assert "Current UI:" in call["messages"][0]["content"] and "<a2ui>" in call["messages"][0]["content"]
    assert f'surface("{sid}", update=true)' in "\n".join(call["system"])


def test_failed_edit_restores_the_snapshot_then_retries():
    eng, llm, sid = built_surface()
    before = eng.surfaces[sid].state.snapshot(sid)
    bad = f'<a2ui>\nsurface("{sid}", update=true)\nroot = HtmlDiv(children=[title, x])\nx = Cre8Button(text="x", variant="huge")\n</a2ui>'
    llm.script["freeform.generate"] = [bad, EDIT.format(sid=sid)]
    a2ui = [e["a2ui"] for e in eng.stream("change it", surface_id=sid) if "a2ui" in e]
    delete_at = next(i for i, m in enumerate(a2ui) if "deleteSurface" in m)
    assert a2ui[delete_at + 1] == before[0], "the pre-edit snapshot is redrawn"
    assert eng.surfaces[sid].state.snapshot(sid)[0]["createSurface"]["dataModel"]["count"] == 4


def test_editing_a_form_hands_it_to_freeform():
    form_slots = {
        "title": "Contact", "intro": "Say hi.", "submit_label": "Send", "success_message": "Thanks",
        "fields": [{"name": "email", "label": "Email", "kind": "email", "required": True}],
    }
    llm = ScriptedLLM({"form.plan": [form_slots], "freeform.select": [SELECT]})
    eng = Engine(llm)
    sid = list(eng.stream("a contact form"))[-1]["trace"]["surfaceId"]
    assert eng.surfaces[sid].pathway == "form"
    components = {c["id"]: c for c in eng.surfaces[sid].state.snapshot(sid)[0]["createSurface"]["components"]}
    intro_text = components["intro"]["children"][0]  # whatever id the assembler gave it
    llm.script["freeform.generate"] = [f'<a2ui>\nsurface("{sid}", update=true)\n{intro_text} = Text(text="Say hello!")\n</a2ui>']
    list(eng.stream("friendlier intro", surface_id=sid))
    assert eng.surfaces[sid].pathway == "freeform"
    texts = {c["id"]: c.get("text") for c in eng.surfaces[sid].state.snapshot(sid)[0]["createSurface"]["components"]}
    assert texts[intro_text] == "Say hello!"


def test_edit_of_unknown_surface_raises():
    eng, _, _ = built_surface()
    with pytest.raises(KeyError):
        list(eng.stream("x", surface_id="nope"))


# ─── Few-shot examples ───────────────────────────────────────────────────────


def test_examples_dir_validates_with_sdk_loader():
    from a2ui.utils.examples import load_examples

    from a2ui_apps.examples import EXAMPLES_DIR, all_examples
    from a2ui_apps.validate import load_catalog

    text = load_examples([load_catalog().api], str(EXAMPLES_DIR), validate=True)
    assert set(all_examples()) == {"contact_form", "sales_dashboard", "pricing_page"}
    assert text.count("---BEGIN ") == 3


def test_closest_example_is_decompiled_into_the_prompt():
    from a2ui_apps.examples import pick_examples

    picked = pick_examples({"Cre8Card", "Cre8List", "Cre8ListItem", "Cre8Badge", "Cre8Grid"})
    assert picked and picked[0][0]["createSurface"]["surfaceId"] == "example_pricing"
    eng, llm = engine(VALID)
    list(eng.stream("a little card"))
    prompt = "\n".join(next(c for c in llm.calls if c["task"] == "freeform.generate")["system"])
    assert "Examples" in prompt and prompt.count("<a2ui>") >= 2, "example decompiled into Express"


def test_direct_json_guide_names_the_surface_and_wrong_surface_is_repaired():
    from a2ui_apps.pathways.freeform import app_guide
    from a2ui_apps.sdk import catalog_id

    assert 'surfaceId "s1"' in app_guide("direct_json", "s1") and catalog_id() in app_guide("direct_json", "s1")
    assert "do not create, name or delete surfaces" in app_guide("express", "s1")
    wrong = '<a2ui>\nsurface("elsewhere")\nroot = Cre8Button(text="x")\n</a2ui>'
    eng, llm = engine(wrong, VALID)
    events = list(eng.stream("a button"))
    assert any("WRONG_SURFACE" in e.get("step", {}).get("detail", "") for e in events)
    deleted = [e["a2ui"]["deleteSurface"]["surfaceId"] for e in events if "deleteSurface" in e.get("a2ui", {})]
    assert "elsewhere" in deleted, "the stray surface is removed from the browser"
    sid = events[-1]["trace"]["surfaceId"]
    assert eng.surfaces[sid].state.snapshot(sid), "the accepted UI is on the engine's surface"
