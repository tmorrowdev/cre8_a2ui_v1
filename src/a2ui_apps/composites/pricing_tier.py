"""PricingTier: one plan in a pricing table."""

from __future__ import annotations

from collections.abc import Sequence

from a2ui.builder.v1_0 import Action
from a2ui.transformers.macros import macro

from a2ui_apps.builders.cre8 import (
    Cre8Badge,
    Cre8Button,
    Cre8Card,
    Cre8Divider,
    Cre8Heading,
    Cre8List,
    Cre8ListItem,
    Cre8TextPassage,
    HtmlDiv,
    Text,
)


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
