"""Section: a titled group of content."""

from __future__ import annotations

from typing import Literal

from a2ui.builder.v1_0 import ChildList
from a2ui.transformers.macros import macro

from a2ui_apps.builders.cre8 import Cre8Heading, HtmlSection, Text


@macro
def Section(title: str, children: ChildList, gap: Literal["4", "8", "12", "16", "24", "32"] = "12") -> HtmlSection:
    """A titled group: a section heading followed by its content, stacked.

    Args:
        title: Section heading.
        children: The section's content.
        gap: Space between the heading and each child.
    """
    return HtmlSection(
        display="flex",
        direction="column",
        gap=gap,
        children=[Cre8Heading(type="title-large", tagVariant="h2", children=[Text(text=title)]), *children],
    )
