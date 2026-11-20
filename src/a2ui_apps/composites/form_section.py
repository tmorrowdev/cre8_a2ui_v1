"""FormSection: a titled form in a card with one submit button."""

from __future__ import annotations

from a2ui.builder.v1_0 import Action, ChildList
from a2ui.transformers.macros import macro

from a2ui_apps.builders.cre8 import Cre8Button, Cre8Card, Cre8Heading, Cre8TextPassage, HtmlDiv, Text


@macro
def FormSection(
    title: str,
    children: ChildList,
    on_submit: Action,
    submit_label: str = "Submit",
    description: str = "",
) -> Cre8Card:
    """A form in a card: title, optional intro, the fields stacked, and a primary submit button.

    Args:
        title: The form's heading, e.g. "Request a demo".
        children: The fields, usually FormField components, in order.
        on_submit: Action fired by the submit button; put the field paths in its context.
        submit_label: Submit button label.
        description: One sentence under the title.
    """
    header = [Cre8Heading(type="title-large", tagVariant="h2", children=[Text(text=title)])]
    if description:
        header.append(Cre8TextPassage(size="small", children=[Text(text=description)]))
    return Cre8Card(
        slot_header=[HtmlDiv(display="flex", direction="column", gap="4", paddingX="24", paddingY="16", children=header)],
        slot_default=[HtmlDiv(display="flex", direction="column", gap="16", paddingX="24", children=children)],
        slot_footer=[HtmlDiv(padding="24", children=[Cre8Button(text=submit_label, variant="primary", on_click=on_submit)])],
    )
