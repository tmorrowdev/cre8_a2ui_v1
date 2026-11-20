"""HeroBanner: the opening block of a landing page."""

from __future__ import annotations

from typing import Literal

from a2ui.builder.v1_0 import Action
from a2ui.transformers.macros import macro

from a2ui_apps.builders.cre8 import Cre8Button, Cre8Heading, Cre8Hero, Cre8TextPassage, HtmlDiv, Text


@macro
def HeroBanner(
    title: str,
    subtitle: str = "",
    cta_label: str = "",
    on_cta: Action | None = None,
    secondary_label: str = "",
    on_secondary: Action | None = None,
    image_src: str = "",
    image_alt: str = "",
    align: Literal["center", "left"] = "center",
) -> Cre8Hero:
    """A landing-page hero: big headline, one supporting sentence and up to two calls to action, optionally over an image.

    Args:
        title: The headline, a few words.
        subtitle: One supporting sentence under the headline.
        cta_label: Primary button label, e.g. "Start free trial". Omit for no button.
        on_cta: Action fired by the primary button.
        secondary_label: Secondary button label, e.g. "See pricing". Omit for none.
        on_secondary: Action fired by the secondary button.
        image_src: Background image URL. Omit for a plain hero.
        image_alt: Description of the background image.
        align: Text alignment of the hero content.
    """
    on_image = bool(image_src)
    content = [Cre8Heading(type="display-default", tagVariant="h1", inverted=on_image or None, children=[Text(text=title)])]
    if subtitle:
        content.append(Cre8TextPassage(inverted=on_image or None, children=[Text(text=subtitle)]))
    buttons = []
    if cta_label:
        buttons.append(Cre8Button(text=cta_label, variant="primary", on_click=on_cta))
    if secondary_label:
        buttons.append(Cre8Button(text=secondary_label, variant="secondary", on_click=on_secondary))
    if buttons:
        content.append(HtmlDiv(display="flex", direction="row", gap="12", wrap=True, justify="center" if align == "center" else "start", children=buttons))
    return Cre8Hero(
        align=align,
        imgSrc=image_src or None,
        imgAlt=image_alt or None,
        hasOverlay=on_image or None,
        children=[
            HtmlDiv(display="flex", direction="column", gap="16", maxWidth="lg", textAlign="center" if align == "center" else "start", children=content)
        ],
    )
