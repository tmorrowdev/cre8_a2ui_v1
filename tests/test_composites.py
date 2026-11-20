"""Every composite and every example: the bar new composites (hand-written or authored) must clear."""

from __future__ import annotations

import inspect

import pytest
from a2ui.builder.v1_0 import Action, ActionEvent

from a2ui_apps.authoring.policy import policy_errors
from a2ui_apps.composites import discover, macro_name
from a2ui_apps.composites.chart_card import ChartCard, ChartSeries
from a2ui_apps.composites.hero_banner import HeroBanner
from a2ui_apps.composites.kpi_row import KpiRow
from a2ui_apps.composites.metric_card import MetricCard
from a2ui_apps.engine import Engine
from a2ui_apps.examples import all_examples, components_of, expanded, pick_examples
from a2ui_apps.llm import ScriptedLLM
from a2ui_apps.macros import macro_names
from a2ui_apps.pathways.base import PathwayFailed
from a2ui_apps.sdk import catalog_id, normalize_components
from a2ui_apps.validate import load_catalog, validate_messages
from conftest import errors_of

COMPOSITES = {macro_name(m): m for m in discover()}


@pytest.mark.parametrize("name", sorted(COMPOSITES))
def test_composite_follows_the_rules(name):
    source = inspect.getsource(inspect.getmodule(COMPOSITES[name]))
    assert policy_errors(source, name) == []
    assert name not in load_catalog().document["components"], "a composite never shadows a cre8 component"


@pytest.mark.parametrize("name", sorted(COMPOSITES))
def test_composite_has_a_gold_example(name):
    users = [example for example, messages in all_examples().items() if name in components_of(messages)]
    assert users, f"{name} needs an example in a2ui_apps/examples/ that uses it (few-shot and test coverage)"


@pytest.mark.parametrize("example", sorted(all_examples()))
def test_example_expands_to_valid_cre8(example, envelope_validator):
    lowered = expanded(all_examples()[example])
    assert not components_of(lowered) & set(macro_names()), "no composite reaches the renderer"
    assert validate_messages(lowered) == []
    for message in lowered:
        assert errors_of(envelope_validator, message) == []


def _flat(node):
    return normalize_components(node.flatten("root"), catalog_id())


def test_kpi_row_sizes_the_grid_to_the_count():
    cards = [MetricCard(label=f"m{i}", value=str(i)) for i in range(3)]
    grid = next(c for c in _flat(KpiRow(children=cards)) if c["component"] == "Cre8Grid")
    assert grid["variant"] == "3up" and len(grid["children"]) == 3
    six = [MetricCard(label=f"m{i}", value=str(i)) for i in range(6)]
    assert next(c for c in _flat(KpiRow(children=six)) if c["component"] == "Cre8Grid")["variant"] == "4up"


def test_chart_card_leaves_colors_to_the_theme():
    series = [ChartSeries(label="A", values=[1, 2]), ChartSeries(label="B", values=[3, 4])]
    line = next(c for c in _flat(ChartCard(title="t", labels=["x", "y"], series=series)) if c["component"] == "Cre8Chart")
    assert "colors" not in line and "options" not in line
    assert [d["label"] for d in line["data"]["datasets"]] == ["A", "B"] and line["showLegend"] is True
    pie = next(c for c in _flat(ChartCard(title="t", kind="pie", labels=["x", "y"], series=series)) if c["component"] == "Cre8Chart")
    assert len(pie["data"]["datasets"]) == 1, "a pie shows one series"


def test_hero_banner_inverts_text_only_over_an_image():
    go = Action(event=ActionEvent(name="go"))
    plain = _flat(HeroBanner(title="Hi", cta_label="Go", on_cta=go))
    assert not any(c.get("inverted") for c in plain)
    over_image = _flat(HeroBanner(title="Hi", image_src="https://example.com/a.jpg", image_alt="a"))
    hero = next(c for c in over_image if c["component"] == "Cre8Hero")
    assert hero["hasOverlay"] is True and any(c.get("inverted") for c in over_image if c["component"] == "Cre8Heading")


def test_composite_examples_are_picked_by_what_they_render():
    # The selection step names cre8 primitives; the composite dashboard example matches them once expanded.
    picked = pick_examples({"Cre8Chart", "Cre8Grid", "Cre8GridItem", "Cre8Card", "Cre8Badge", "Cre8Alert"})
    assert picked and picked[0][0]["createSurface"]["surfaceId"] == "example_agency_overview"


# --- the runtime repair loop, with composites ---------------------------------------------

GOOD = '''A dashboard.
<a2ui>
root = HtmlDiv(display="flex", direction="column", gap="24", children=[kpis, chart])
kpis = KpiRow(children=[m1, m2])
m1 = MetricCard(label="Revenue", value="$48.2k", delta="+6.1%", trend="up")
m2 = MetricCard(label="Orders", value="1,204")
chart = ChartCard(title="Revenue by week", labels=["W1", "W2"], series=[{label: "Revenue", values: [10, 12]}])
</a2ui>'''
BAD_KIND = '<a2ui>\nroot = HtmlDiv(children=[chart])\nchart = ChartCard(title="x", kind="sankey", labels=["a"], series=[{label: "s", values: [1]}])\n</a2ui>'
BAD_SERIES = '<a2ui>\nroot = HtmlDiv(children=[chart])\nchart = ChartCard(title="x", labels=["a"], series=[{name: "s"}])\n</a2ui>'


def run(*generate):
    llm = ScriptedLLM({
        "route": [{"pathway": "freeform", "confidence": 0.9, "reason": "x"}],
        "freeform.select": [{"components": ["Cre8Card"]}],
        "freeform.generate": list(generate),
    })
    return Engine(llm), llm


def test_invalid_composite_arguments_are_repaired_with_the_error():
    eng, llm = run(BAD_KIND, GOOD)
    events = list(eng.stream("a revenue overview"))
    generate_calls = [c for c in llm.calls if c["task"] == "freeform.generate"]
    assert len(generate_calls) == 2
    feedback = generate_calls[1]["messages"][-1]["content"]
    assert "rejected" in feedback and "sankey" in feedback
    sid = events[-1]["trace"]["surfaceId"]
    snapshot = eng.surfaces[sid].state.snapshot(sid)
    assert validate_messages(snapshot) == []
    assert {"Cre8Chart", "Cre8Grid"} <= components_of(snapshot)


def test_repair_is_bounded():
    eng, llm = run(BAD_KIND, BAD_SERIES, BAD_KIND)
    with pytest.raises(PathwayFailed) as exc:
        list(eng.stream("a revenue overview"))
    assert exc.value.errors
    assert len([c for c in llm.calls if c["task"] == "freeform.generate"]) == 3
