"""KpiRow: a responsive row of headline metrics."""

from __future__ import annotations

from a2ui.builder.v1_0 import ChildList
from a2ui.transformers.macros import macro

from a2ui_apps.builders.cre8 import Cre8Grid, Cre8GridItem, Cre8Heading, HtmlSection, Text

GRID_FOR_COUNT = {1: "side-by-side", 2: "2up", 3: "3up"}


@macro
def KpiRow(children: ChildList, title: str = "") -> HtmlSection:
    """A row of headline metrics laid out on the cre8 grid; columns follow the count (up to 4 per row).

    Args:
        children: The metrics, usually MetricCard components, in reading order.
        title: Optional heading above the row, e.g. "This week".
    """
    if isinstance(children, list):
        cells = [Cre8GridItem(children=[child]) for child in children]
        variant = GRID_FOR_COUNT.get(len(cells), "4up")
    else:  # a templated (data-driven) list keeps its template; the grid wraps as needed
        cells, variant = children, "4up"
    content = [Cre8Grid(variant=variant, gap="lg", children=cells)]
    if title:
        content.insert(0, Cre8Heading(type="title-large", tagVariant="h2", children=[Text(text=title)]))
    return HtmlSection(display="flex", direction="column", gap="12", children=content)
