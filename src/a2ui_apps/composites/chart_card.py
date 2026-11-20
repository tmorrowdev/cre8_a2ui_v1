"""ChartCard: a titled chart in a card."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from a2ui.transformers.macros import macro
from pydantic import BaseModel, Field

from a2ui_apps.builders.cre8 import Cre8Card, Cre8Chart, Cre8Heading, Cre8TextPassage, HtmlDiv, Text


class ChartSeries(BaseModel):
    """One data series: a legend label and one value per x-axis label."""

    label: str = Field(description="Legend label, e.g. 'Revenue'")
    values: list[float] = Field(description="One number per entry in the chart's labels")


@macro
def ChartCard(
    title: str,
    labels: Sequence[str],
    series: Sequence[ChartSeries],
    kind: Literal["line", "bar", "pie", "doughnut"] = "line",
    caption: str = "",
    height: int = 280,
) -> Cre8Card:
    """A chart in a card with a title and an optional caption. Colors come from the theme.

    Args:
        title: What the chart shows, e.g. "Revenue by week".
        labels: The x-axis labels (or slice names for pie and doughnut).
        series: The data series; pie and doughnut use only the first.
        kind: Chart type.
        caption: One sentence under the chart, e.g. the takeaway or the data source.
        height: Chart height in pixels.
    """
    datasets = [{"label": s.label, "data": list(s.values)} for s in (series[:1] if kind in ("pie", "doughnut") else series)]
    body = [
        Cre8Chart(
            type=kind,
            data={"labels": list(labels), "datasets": datasets},
            height=height,
            responsive=True,
            ariaLabel=title,
            showLegend=len(datasets) > 1 or kind in ("pie", "doughnut"),
        )
    ]
    if caption:
        body.append(Cre8TextPassage(size="small", children=[Text(text=caption)]))
    return Cre8Card(
        slot_header=[HtmlDiv(paddingX="16", paddingY="12", children=[Cre8Heading(type="title-default", tagVariant="h3", children=[Text(text=title)])])],
        slot_default=[HtmlDiv(display="flex", direction="column", gap="12", padding="16", children=body)],
    )
