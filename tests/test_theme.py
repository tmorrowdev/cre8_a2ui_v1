"""The agent's theme tool: detect styling intent, plan seeds, validate, deliver."""

from __future__ import annotations

import pytest

from a2ui_apps.engine import Engine
from a2ui_apps.llm import ScriptedLLM
from a2ui_apps.theme import EXTENSION_KEY, ThemeSpec, normalize, plan_theme, wants_theme
from a2ui_apps.validate import validate_messages
from conftest import errors_of


@pytest.mark.parametrize("prompt", [
    "A contact form for a bakery in warm terracotta",
    "A dashboard using #e11d48 as the brand color",
    "Pricing page, dark mode, rounded corners",
    "An editorial recipe card with a serif font",
])
def test_detects_styling_intent(prompt):
    assert wants_theme(prompt)


@pytest.mark.parametrize("prompt", ["A contact form for a bakery", "A sales dashboard for an online store", "A team directory"])
def test_no_hint_means_no_model_call(prompt):
    assert not wants_theme(prompt)
    llm = ScriptedLLM()  # no theme.plan scripted: a call would raise
    assert plan_theme(prompt, llm) is None and llm.calls == []


def test_normalize_keeps_only_trustworthy_values():
    seeds = normalize(ThemeSpec(primary="#1E3", accent="not a color", neutral="64748b", radius=99, font="Serif", mode="dark"))
    assert set(seeds) == {"mode", "primary", "neutral", "radius", "font"}
    assert seeds["neutral"] == "#64748b" and seeds["radius"] == 32
    assert normalize(ThemeSpec(radius=-5))["radius"] == 0
    assert normalize(ThemeSpec()) == {}


TERRACOTTA = {"primary": "#c2410c", "neutral": "#78716c", "radius": 28, "font": "Serif", "rationale": "warm, rustic"}
FORM = {
    "title": "Contact", "intro": "Say hi.", "submit_label": "Send", "success_message": "Thanks",
    "fields": [{"name": "email", "label": "Email", "kind": "email", "required": True}],
}


def test_theme_is_stamped_as_an_extension_on_create(envelope_validator):
    llm = ScriptedLLM({"theme.plan": [TERRACOTTA], "form.plan": [FORM]})
    events = list(Engine(llm).stream("A contact form for a bakery in warm terracotta with a serif font"))
    assert {"theme": {"primary": "#c2410c", "neutral": "#78716c", "radius": 28, "font": "Serif"}} in events
    step = next(e["step"] for e in events if e.get("step", {}).get("name") == "theme")
    assert "primary #c2410c" in step["detail"] and "warm, rustic" in step["detail"] and not step["deterministic"]
    create = next(e["a2ui"] for e in events if "createSurface" in e.get("a2ui", {}))
    assert create["createSurface"]["metadata"]["extensions"][EXTENSION_KEY]["primary"] == "#c2410c"
    assert errors_of(envelope_validator, create) == []
    assert validate_messages([create]) == []


def test_theme_reaches_freeform_surfaces_too():
    from test_freeform import ROUTE_FREEFORM, SELECT, VALID

    llm = ScriptedLLM({"theme.plan": [{"mode": "dark", "primary": "#16a34a"}], "route": [ROUTE_FREEFORM],
                       "freeform.select": [SELECT], "freeform.generate": [VALID]})
    events = list(Engine(llm).stream("a little card in forest green, dark mode"))
    create = next(e["a2ui"] for e in events if "createSurface" in e.get("a2ui", {}))
    # Dark mode: buttons use a derived light shade, so the seed is kept as chosen.
    assert create["createSurface"]["metadata"]["extensions"][EXTENSION_KEY] == {"mode": "dark", "primary": "#16a34a"}


def test_theme_only_edit_needs_no_ui_change():
    from test_freeform import ROUTE_FREEFORM, SELECT, VALID

    llm = ScriptedLLM({"route": [ROUTE_FREEFORM], "freeform.select": [SELECT, SELECT], "freeform.generate": [VALID]})
    eng = Engine(llm)
    sid = list(eng.stream("a little card"))[-1]["trace"]["surfaceId"]
    llm.script["theme.plan"] = [{"primary": "#7c3aed"}]
    llm.script["freeform.generate"] = ["Applied the purple theme."]  # the model rightly changes no UI
    events = list(eng.stream("make it purple", surface_id=sid))
    assert {"theme": {"primary": "#7c3aed"}} in events
    assert not any(e.get("step", {}).get("name") == "repair" for e in events)
    assert eng.surfaces[sid].theme == {"primary": "#7c3aed"}
    guide = "\n".join(next(c for c in reversed(llm.calls) if c["task"] == "freeform.generate")["system"])
    assert "already applied the colors" in guide


def test_envelope_validator_rejects_a_bad_extension_key(envelope_validator):
    from a2ui_apps.sdk import catalog_id

    def create(extensions):
        return {"version": "1.0", "createSurface": {"surfaceId": "s", "catalogId": catalog_id(),
                "metadata": {"extensions": extensions}, "components": [{"id": "root", "component": "Cre8Button"}]}}

    assert errors_of(envelope_validator, create({EXTENSION_KEY: {"primary": "#000000"}})) == []
    assert errors_of(envelope_validator, create({"bad-key": 1})), "a non-UAX#31 extension key must be rejected"



def test_pastel_primary_is_darkened_to_readable_contrast():
    from a2ui_apps.theme import MIN_TEXT_CONTRAST, contrast_with_white

    pastel = "#a78bfa"
    assert contrast_with_white(pastel) < MIN_TEXT_CONTRAST
    fixed = normalize(ThemeSpec(primary=pastel))["primary"]
    assert contrast_with_white(fixed) >= MIN_TEXT_CONTRAST
    r1, g1, b1 = (int(pastel[i : i + 2], 16) for i in (1, 3, 5))
    r2, g2, b2 = (int(fixed[i : i + 2], 16) for i in (1, 3, 5))
    assert abs(r2 / b2 - r1 / b1) < 0.05, "darkened, not re-hued"
    assert normalize(ThemeSpec(primary="#1e3a8a"))["primary"] == "#1e3a8a", "already readable: untouched"



def test_contrast_guard_applies_in_light_and_auto_but_not_dark():
    pastel = "#a78bfa"
    assert normalize(ThemeSpec(primary=pastel, mode="dark"))["primary"] == pastel
    assert normalize(ThemeSpec(primary=pastel, mode="light"))["primary"] != pastel
    assert normalize(ThemeSpec(primary=pastel))["primary"] != pastel  # unspecified mode may render light
