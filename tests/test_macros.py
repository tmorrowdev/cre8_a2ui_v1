"""cre8 builders (generated) and macros (expanded before transport)."""

from __future__ import annotations

from a2ui.builder.v1_0 import Action, ActionEvent, DataBinding

from a2ui_apps.builders.cre8 import Cre8Badge, Cre8Button, Cre8Card, Cre8Grid, Cre8Heading, HtmlDiv, Text
from a2ui_apps.engine import Engine
from a2ui_apps.llm import ScriptedLLM
from a2ui_apps.macros import inference_catalog, macro_names
from a2ui_apps.sdk import catalog_id, normalize_components
from a2ui_apps.validate import validate_messages
from conftest import errors_of

MACRO_UI = '''Pricing with macros.
<a2ui>
root = HtmlDiv(display="grid", columns=2, gap="16", children=[basic, pro, rev, signup])
basic = PricingTier(name="Basic", price="$9", features=["1 user", "5 GB"], cta_label="Choose Basic", on_choose=Event("choose", {plan: "basic"}))
pro = PricingTier(name="Pro", price="$29", features=["10 users", "100 GB"], cta_label="Choose Pro", on_choose=Event("choose", {plan: "pro"}), highlighted=true, badge="Most popular")
rev = MetricCard(label="Revenue", value="$48.2k", delta="+6.1%", trend="up")
signup = Section(title="Stay in touch", children=[email])
email = FormField(label="Email", path="/form/email", kind="email", required=true)
$/form/email = ""
</a2ui>'''


def run(*generate):
    llm = ScriptedLLM({
        "route": [{"pathway": "freeform", "confidence": 0.9, "reason": "x"}],
        "freeform.select": [{"components": ["Cre8Card"]}],
        "freeform.generate": list(generate),
    })
    eng = Engine(llm)
    return eng, llm, list(eng.stream("pricing"))


def test_builders_flatten_to_valid_cre8():
    tree = HtmlDiv(display="flex", direction="column", gap="16", children=[
        Cre8Heading(type="headline-large", children=[Text(text="Built with builders")]),
        Cre8Grid(variant="2up", break_="faster", children=[]),
        Cre8Card(slot_default=[Cre8Badge(text=DataBinding(path="/status"), status="info")]),
        Cre8Button(text="Go", variant="primary", on_click=Action(event=ActionEvent(name="go"))),
    ])
    components = normalize_components(tree.flatten("root"), catalog_id())
    grid = next(c for c in components if c["component"] == "Cre8Grid")
    assert grid["break"] == "faster", "python keyword props round-trip through their alias"
    assert not any("catalogId" in c for c in components), "redundant pre-final catalogId is dropped"
    message = {"version": "1.0", "createSurface": {"surfaceId": "s", "catalogId": catalog_id(), "components": components, "dataModel": {"status": "ok"}}}
    assert validate_messages([message]) == []


def test_macros_are_in_the_inference_catalog_only():
    names = set(macro_names())
    assert {"MetricCard", "PricingTier", "FormField", "Section", "KpiRow", "HeroBanner", "ChartCard", "FormSection"} <= names
    assert names <= set(inference_catalog().components)


def test_macros_expand_to_cre8_primitives_before_transport(envelope_validator):
    eng, llm, events = run(MACRO_UI)
    assert not [e for e in events if "error" in e]
    messages = [e["a2ui"] for e in events if "a2ui" in e]
    types = {c["component"] for m in messages for k in ("createSurface", "updateComponents") for c in (m.get(k) or {}).get("components", [])}
    assert not types & set(macro_names()), "no macro reaches the renderer"
    assert {"Cre8Card", "Cre8List", "Cre8Field", "HtmlSection"} <= types
    for m in messages:
        assert errors_of(envelope_validator, m) == []
    sid = events[-1]["trace"]["surfaceId"]
    snapshot = eng.surfaces[sid].state.snapshot(sid)
    assert validate_messages(snapshot) == []
    fields = [c for c in snapshot[0]["createSurface"]["components"] if c["component"] == "Cre8Field"]
    assert fields[0]["value"] == {"@path": "/form/email"}
    prompt = "\n".join(next(c for c in llm.calls if c["task"] == "freeform.generate")["system"])
    assert "PricingTier(" in prompt and "MetricCard(" in prompt


def test_bad_macro_argument_triggers_repair():
    bad = '<a2ui>\nroot = HtmlDiv(children=[m])\nm = MetricCard(label="x", value="1", trend="sideways")\n</a2ui>'
    eng, llm, events = run(bad, MACRO_UI)
    repair = [e["step"]["detail"] for e in events if e.get("step", {}).get("name") == "repair"]
    assert repair and "sideways" in repair[0]
