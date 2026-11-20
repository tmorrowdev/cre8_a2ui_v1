"""MetricCard: one headline number."""

from __future__ import annotations

from typing import Literal

from a2ui.transformers.macros import macro

from a2ui_apps.builders.cre8 import Cre8Badge, Cre8Card, Cre8Heading, HtmlDiv, Text


@macro
def MetricCard(
    label: str,
    value: str,
    delta: str = "",
    trend: Literal["up", "down", "flat"] = "flat",
    good_when_up: bool = True,
) -> Cre8Card:
    """A headline number in a card: label, large value, and an optional colored change badge.

    Args:
        label: What the number measures, e.g. "Revenue".
        value: The formatted value, e.g. "$48.2k".
        delta: The change versus the previous period, e.g. "+6.1%". Omit for none.
        trend: Direction of the change.
        good_when_up: Whether an increase is good (colors the badge green rather than red).
    """
    status = "info" if trend == "flat" else ("success" if (trend == "up") == good_when_up else "error")
    content = [
        Cre8Heading(type="label-default", children=[Text(text=label)]),
        Cre8Heading(type="headline-default", children=[Text(text=value)]),
    ]
    if delta:
        content.append(Cre8Badge(text=delta, status=status))
    return Cre8Card(slot_default=[HtmlDiv(display="flex", direction="column", gap="4", padding="16", children=content)])
