"""Structural HTML elements and token-constrained spacing/layout props for the catalog.

Two rules keep this flexible without competing with cre8 or making it unsafe:

- Only structural elements: sectioning and layout containers. Content (text,
  headings, lists, links, images) stays with cre8 components, so typography and
  interaction are always branded. No element here takes a URL or raw HTML.
- Styling is never free CSS. Every style prop is an enum over cre8 design
  tokens (`padding: "16"` -> `var(--cre8-spacing-16)`), so values validate,
  cannot inject CSS, and follow the surface's seeds and mode.

Each style property carries `x-style` naming what it sets; each element
carries `x-html-tag`. The renderer reads
those annotations rather than hard-coding names.
"""

from __future__ import annotations

from typing import Any

COMMON = "common_types.json#/$defs/"

SPACE = ["0", "4", "8", "12", "16", "24", "32", "48", "64", "96"]
RADIUS = ["none", "small", "field", "large", "container", "pill"]
# Only tokens that stay readable in both modes. Several cre8 bg tokens don't
# flip (the status tints stay near-white in dark mode) and `bg-brand` is white
# in light mode, so "brand" maps to the flipping brand tint (bg-brand-hover).
BACKGROUND = ["default", "subtle", "brand"]
BORDER_COLOR = ["default", "strong", "brand"]

LEAF_DEFS: dict[str, Any] = {
    "Space": {
        "type": "string",
        "enum": SPACE,
        "description": "A cre8 spacing step; at default density the number is pixels (16 = 1rem).",
    },
    "Radius": {"type": "string", "enum": RADIUS, "description": "A cre8 corner-radius token."},
    "Background": {"type": "string", "enum": BACKGROUND, "description": "Container background: default (page), subtle (raised panel) or brand (brand tint). All flip with light/dark mode."},
    "BorderColor": {"type": "string", "enum": BORDER_COLOR, "description": "A cre8 border colour token."},
}


def _style(ref_or_schema: str | dict[str, Any], style: str, description: str) -> dict[str, Any]:
    base = {"$ref": f"#/$defs/{ref_or_schema}"} if isinstance(ref_or_schema, str) else dict(ref_or_schema)
    return {**base, "description": description, "x-style": style}


# Spacing goes on every component, cre8 or HTML. No cre8 prop uses these names.
SPACING_PROPS: dict[str, Any] = {
    "padding": _style("Space", "padding", "Padding on all sides."),
    "paddingX": _style("Space", "paddingX", "Horizontal (inline) padding."),
    "paddingY": _style("Space", "paddingY", "Vertical (block) padding."),
    "margin": _style("Space", "margin", "Margin on all sides."),
    "marginX": _style("Space", "marginX", "Horizontal (inline) margin."),
    "marginY": _style("Space", "marginY", "Vertical (block) margin."),
}

# Layout and surface styling, HTML elements only: several cre8 components
# already own `gap`, `width`, `align`, `columns` or `display`. No typography:
# text styling belongs to cre8's text components.
BOX_PROPS: dict[str, Any] = {
    "display": _style({"type": "string", "enum": ["block", "inline", "inline-block", "flex", "inline-flex", "grid", "none"]}, "display", "CSS display."),
    "direction": _style({"type": "string", "enum": ["row", "column"]}, "direction", "Flex direction; implies display flex."),
    "gap": _style("Space", "gap", "Space between children of a flex or grid box."),
    "align": _style({"type": "string", "enum": ["start", "center", "end", "stretch", "baseline"]}, "align", "Cross-axis alignment (align-items)."),
    "justify": _style({"type": "string", "enum": ["start", "center", "end", "between", "around", "evenly"]}, "justify", "Main-axis distribution (justify-content)."),
    "wrap": _style({"type": "boolean"}, "wrap", "Let flex children wrap."),
    "columns": _style({"type": "integer", "minimum": 1, "maximum": 6}, "columns", "Equal grid columns; implies display grid."),
    "background": _style("Background", "background", "Background colour token."),
    "radius": _style("Radius", "radius", "Corner radius token."),
    "border": _style("BorderColor", "border", "A 1px border in this colour token."),
    "width": _style({"type": "string", "enum": ["auto", "full", "fit"]}, "width", "auto, 100% (full) or fit-content."),
    "maxWidth": _style({"type": "string", "enum": ["sm", "md", "lg", "xl", "prose", "none"]}, "maxWidth", "sm 24rem, md 40rem, lg 64rem, xl 80rem, prose 65ch."),
    "textAlign": _style({"type": "string", "enum": ["start", "center", "end"]}, "textAlign", "Text alignment."),
}

# tag -> (type name, description). All are containers with children.
ELEMENTS: list[tuple[str, str, str]] = [
    ("div", "HtmlDiv", "Generic layout container; use display/direction/gap/columns."),
    ("section", "HtmlSection", "A thematic grouping of content."),
    ("article", "HtmlArticle", "A self-contained composition, e.g. a card or post."),
    ("aside", "HtmlAside", "Content tangential to its surroundings, e.g. a sidebar."),
    ("header", "HtmlHeader", "Introductory content for its section."),
    ("footer", "HtmlFooter", "Closing content for its section."),
    ("nav", "HtmlNav", "A group of navigation links (the links themselves are cre8 components)."),
]


def html_components() -> dict[str, Any]:
    components: dict[str, Any] = {}
    for tag, type_name, description in ELEMENTS:
        components[type_name] = {
            "type": "object",
            "title": type_name,
            "description": f"<{tag}> — {description}",
            "x-html-tag": tag,
            "x-category": "Structure",
            "allOf": [
                {"$ref": "#/$defs/NativeEventHandlers"},
                {"$ref": "#/$defs/SpacingProps"},
                {"$ref": "#/$defs/BoxStyle"},
                {
                    "type": "object",
                    "properties": {
                        "component": {"const": type_name},
                        "children": {"$ref": f"{COMMON}ChildList", "description": "A list of child components, in order, even if there is only one."},
                    },
                    "required": ["component"],
                },
            ],
        }
    return components


def style_defs() -> dict[str, Any]:
    return {
        **LEAF_DEFS,
        "SpacingProps": {
            "type": "object",
            "description": "Token-based spacing, accepted by every component.",
            "properties": SPACING_PROPS,
        },
        "BoxStyle": {
            "type": "object",
            "description": "Token-based layout and surface styling for structural HTML elements.",
            "properties": BOX_PROPS,
        },
    }
