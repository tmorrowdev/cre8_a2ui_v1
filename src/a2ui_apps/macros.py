"""cre8 macros: composite components the model can use, lowered to cre8 primitives.

The model sees these as ordinary catalog components (the expander adds their
schemas to the inference catalog), so one `MetricCard(...)` line replaces a
dozen nested components. Before anything reaches the renderer or the agent's
state, `expand` lowers every macro into cre8 primitives, so the browser only
ever needs the cre8 catalog.
"""

from __future__ import annotations

from collections.abc import Sequence
from functools import lru_cache
from typing import Any, Literal

from a2ui.builder.v1_0 import Action, ChildList, DataBinding
from a2ui.transformers.macros import MacroExpander, macro

from a2ui_apps.builders.cre8 import (
    Cre8Badge,
    Cre8Button,
    Cre8Card,
    Cre8Divider,
    Cre8Field,
    Cre8Heading,
    Cre8List,
    Cre8ListItem,
    Cre8TextPassage,
    HtmlDiv,
    HtmlSection,
    Text,
)
from a2ui_apps.validate import load_catalog

Gap = Literal["4", "8", "12", "16", "24", "32"]


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


@macro
def PricingTier(
    name: str,
    price: str,
    features: Sequence[str],
    cta_label: str,
    on_choose: Action,
    period: str = "/ month",
    highlighted: bool = False,
    badge: str = "",
) -> Cre8Card:
    """One plan in a pricing table: name, price, feature list and a choose button.

    Args:
        name: Plan name, e.g. "Pro".
        price: Formatted price, e.g. "$29".
        features: One short line per included feature.
        cta_label: Button label, e.g. "Choose Pro".
        on_choose: Action fired when the plan is chosen.
        period: Billing period shown after the price.
        highlighted: Emphasize this plan (primary button, brand-colored name).
        badge: Optional badge next to the name, e.g. "Most popular".
    """
    header = [Cre8Heading(type="title-large", tagVariant="h2", brandColor=highlighted, children=[Text(text=name)])]
    if badge:
        header.append(Cre8Badge(text=badge, status="info"))
    return Cre8Card(
        fullHeight=True,
        slot_header=[HtmlDiv(display="flex", direction="row", justify="between", align="center", paddingX="24", paddingY="16", children=header)],
        slot_default=[
            HtmlDiv(
                display="flex",
                direction="column",
                gap="16",
                paddingX="24",
                children=[
                    HtmlDiv(display="flex", direction="row", align="baseline", gap="4", children=[
                        Cre8Heading(type="display-small", tagVariant="h3", children=[Text(text=price)]),
                        Cre8TextPassage(size="small", children=[Text(text=period)]),
                    ]),
                    Cre8Divider(),
                    Cre8List(children=[Cre8ListItem(children=[Text(text=f)]) for f in features]),
                ],
            )
        ],
        slot_footer=[
            Cre8Button(text=cta_label, variant="primary" if highlighted else "secondary", fullWidth=True, margin="24", on_click=on_choose)
        ],
    )


@macro
def FormField(
    label: str,
    path: str,
    kind: Literal["text", "email", "number", "tel", "url", "date", "password"] = "text",
    required: bool = False,
    placeholder: str = "",
) -> Cre8Field:
    """A labelled input whose value is two-way bound to the data model.

    Args:
        label: Visible label.
        path: Absolute data model path the value is bound to, e.g. "/form/email".
        kind: Input type.
        required: Whether the field must be filled.
        placeholder: Hint text shown when empty.
    """
    return Cre8Field(
        label=label,
        type=kind,
        required=required or None,
        placeholder=placeholder or None,
        value=DataBinding(path=path),
    )


@macro
def Section(title: str, children: ChildList, gap: Gap = "12") -> HtmlSection:
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


MACROS = [MetricCard, PricingTier, FormField, Section]


@lru_cache(maxsize=1)
def expander() -> MacroExpander:
    """Raises on a bad invocation, so the freeform repair loop sees the error."""
    base = load_catalog().api
    return MacroExpander(MACROS, base_catalogs=[base], protocol_version="1.0", on_error="raise")


@lru_cache(maxsize=1)
def inference_catalog() -> Any:
    """The cre8 catalog plus macro components: what the prompt and parser see."""
    return expander().transform_to_inference_catalog(load_catalog().api)


def macro_names() -> list[str]:
    return [m.__name__ if hasattr(m, "__name__") else str(m) for m in MACROS]


def expand(messages: Sequence[Any]) -> list[Any]:
    """Lower macro components to cre8 primitives (models or dicts in, as the SDK returns)."""
    return list(expander().transform_to_transport(list(messages)))
