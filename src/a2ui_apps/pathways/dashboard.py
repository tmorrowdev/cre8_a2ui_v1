"""Dashboard pathway: the model supplies metrics and sections; Python lays them out."""

from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, Field

from a2ui_apps.llm import LLM
from a2ui_apps.pathways.base import Message, Tree, create_surface

MAX_METRICS = 8
MAX_SECTIONS = 6
MAX_ROWS = 25


class Metric(BaseModel):
    label: str
    value: str = Field(description="Display value, already formatted, e.g. '$12.4k' or '98.2%'")
    delta: str | None = Field(default=None, description="Change vs previous period, e.g. '+4.1%'")
    trend: Literal["up", "down", "flat"] = "flat"
    good_when_up: bool = True


class ProgressItem(BaseModel):
    label: str
    value: float
    max: float = 100


class Section(BaseModel):
    title: str
    kind: Literal["table", "progress"]
    columns: list[str] = Field(default_factory=list, description="table only")
    rows: list[list[str]] = Field(default_factory=list, description="table only; one string per column")
    items: list[ProgressItem] = Field(default_factory=list, description="progress only")


class DashboardSlots(BaseModel):
    title: str
    subtitle: str
    metrics: list[Metric]
    sections: list[Section] = Field(default_factory=list)


PLAN_SYSTEM = """You design read-only dashboards. Given a request, return a title, a one-sentence subtitle,
2-8 headline metrics (formatted display values, optional delta and trend), and up to 6 sections.
A section is either a table (columns + rows of strings, at most 25 rows) or a progress list
(label, value, max). Invent realistic sample data when the request does not supply any, and say
so in the subtitle."""

GRID_FOR_COUNT = {1: "side-by-side", 2: "2up", 3: "3up", 4: "4up"}
NARROW_PX = 720


def normalize(slots: DashboardSlots) -> DashboardSlots:
    sections = []
    for s in slots.sections[:MAX_SECTIONS]:
        if s.kind == "table":
            columns = s.columns or ["Value"]
            rows = [(r + [""] * len(columns))[: len(columns)] for r in s.rows[:MAX_ROWS]]
            if rows:
                sections.append(s.model_copy(update={"columns": columns, "rows": rows, "items": []}))
        else:
            items = [i.model_copy(update={"max": i.max if i.max > 0 else 100}) for i in s.items[:MAX_ROWS]]
            if items:
                sections.append(s.model_copy(update={"items": items, "columns": [], "rows": []}))
    return slots.model_copy(update={"metrics": slots.metrics[:MAX_METRICS], "sections": sections})


def _badge_status(m: Metric) -> str:
    if m.trend == "flat":
        return "info"
    return "success" if (m.trend == "up") == m.good_when_up else "error"


class DashboardPathway:
    name: ClassVar[str] = "dashboard"
    description: ClassVar[str] = "Show numbers at a glance: KPIs, metrics, analytics, status overviews, reports."
    # Words that name a dashboard, not words a dashboard contains: "a pricing page
    # with usage stats" is not a dashboard.
    keywords: ClassVar[tuple[str, ...]] = ("dashboard", "kpi", "kpis", "analytics", "admin panel", "monitoring")

    def plan(self, prompt: str, llm: LLM) -> DashboardSlots:
        slots = llm.structured(task="dashboard.plan", system=[PLAN_SYSTEM], prompt=prompt, schema=DashboardSlots, effort="low")
        return normalize(slots)

    def assemble(self, slots: DashboardSlots, surface_id: str, context: dict[str, Any] | None = None) -> list[Message]:
        tree = Tree()
        children = [
            tree.heading(slots.title, type="headline-large", tag="h1", id="title"),
            tree.passage(slots.subtitle, id="subtitle"),
        ]

        if slots.metrics:
            items = []
            for m in slots.metrics:
                card_content = [
                    tree.heading(m.label, type="label-default", id="metric_label"),
                    tree.heading(m.value, type="headline-default", id="metric_value"),
                ]
                if m.delta:
                    card_content.append(tree.add("Cre8Badge", id="metric_delta", text=m.delta, status=_badge_status(m)))
                card = tree.add("Cre8Card", id="metric_card", slot_default=card_content)
                items.append(tree.add("Cre8GridItem", id="metric_cell", children=[card]))
            variant = GRID_FOR_COUNT.get(len(items), "4up")
            # Renderer RPC: on a narrow viewport, never more than two metrics per row.
            width = ((context or {}).get("getViewport") or {}).get("width")
            if isinstance(width, (int, float)) and width < NARROW_PX and variant in ("3up", "4up"):
                variant = "2up"
            children.append(tree.add("Cre8Grid", id="metrics", variant=variant, gap="lg", children=items))

        for section in slots.sections:
            section_children = [tree.heading(section.title, type="title-large", tag="h2", id="section_title")]
            if section.kind == "table":
                header_cells = [tree.add("Cre8TableHeaderCell", id="th", children=[tree.text(c)]) for c in section.columns]
                header_row = tree.add("Cre8TableRow", id="header_row", slot_default=header_cells)
                body_rows = []
                for row in section.rows:
                    cells = [tree.add("Cre8TableCell", id="td", children=[tree.text(v)]) for v in row]
                    body_rows.append(tree.add("Cre8TableRow", id="row", slot_default=cells))
                header = tree.add("Cre8TableHeader", id="table_header", children=[header_row])
                body = tree.add("Cre8TableBody", id="table_body", children=body_rows)
                section_children.append(tree.add("Cre8Table", id="table", variant="striped", children=[header, body]))
            else:
                for item in section.items:
                    label = tree.heading(item.label, type="label-default", id="progress_label")
                    bar = tree.add("Cre8PercentBar", id="progress", value=item.value, max=item.max, disableActionLeft=True)
                    section_children.append(tree.stack([label, bar], gap="4", id="progress_item"))
            children.append(tree.stack(section_children, gap="12", id="section", element="HtmlSection"))

        body = tree.stack(children, gap="24", id="dashboard_body")
        tree.components.insert(0, {"id": "root", "component": "Cre8LayoutSection", "children": [body]})
        return [create_surface(surface_id, tree.components)]

    def on_action(self, slots: DashboardSlots, action: dict[str, Any], data: dict[str, Any], surface_id: str) -> list[Message]:
        return []
