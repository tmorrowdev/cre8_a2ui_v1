"""The agent's theme tool: turn styling intent in a prompt into cre8-a2ui seeds.

Semi-deterministic, like the rest of the pipeline:

1. `wants_theme` - cheap rules decide whether the prompt says anything about
   look and feel. If not, no model call is made.
2. `plan_theme` - one low-effort structured call fills a ThemeSpec with only the
   seeds the prompt implies.
3. `normalize` - Python validates every value (hex colors, radius range, font
   list) and drops anything it cannot trust.

A2UI v1.0 forbids `theme` on createSurface (branding belongs to the renderer),
so the result travels as a surface extension, `metadata.extensions.cre8_theme`,
which any renderer may read and the cre8 renderer applies as seed tokens.
"""

from __future__ import annotations

import re
from typing import Any, Literal

from pydantic import BaseModel, Field

from a2ui_apps.google_fonts import GoogleFonts
from a2ui_apps.llm import LLM

EXTENSION_KEY = "cre8_theme"
FONTS = ("Plus Jakarta Sans", "System", "Serif", "Mono")
HEX = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")

_COLOR_WORDS = (
    "red", "crimson", "rose", "pink", "magenta", "purple", "violet", "lavender", "indigo", "blue", "navy",
    "sky", "cyan", "teal", "turquoise", "green", "emerald", "mint", "olive", "lime", "yellow", "gold",
    "amber", "orange", "coral", "peach", "terracotta", "brown", "beige", "cream", "black", "charcoal",
    "slate", "grey", "gray", "white", "pastel", "neon", "earthy", "warm", "cool", "muted", "vibrant",
)
_STYLE_PHRASES = (
    "theme", "themed", "brand", "branded", "branding", "color", "colour", "colors", "colours", "palette",
    "dark mode", "light mode", "dark theme", "light theme", "dark background", "rounded", "round corners",
    "square corners", "sharp corners", "pill", "serif", "sans-serif", "monospace", "mono font", "font",
    "typeface", "look and feel", "style it", "styled",
)
_HINT = re.compile(
    r"#[0-9a-fA-F]{3}\b|#[0-9a-fA-F]{6}\b|\b(" + "|".join(re.escape(w) for w in _COLOR_WORDS + _STYLE_PHRASES) + r")\b",
    re.IGNORECASE,
)


class ThemeSpec(BaseModel):
    """Only what the request implies; null means 'leave as is'."""

    mode: Literal["auto", "light", "dark"] | None = Field(default=None, description="Only if the request asks for light or dark")
    primary: str | None = Field(default=None, description="Main brand color as #rrggbb (buttons, links, accents)")
    accent: str | None = Field(default=None, description="Secondary highlight color as #rrggbb")
    neutral: str | None = Field(default=None, description="Gray family as #rrggbb; tint it warm or cool to match the mood")
    radius: int | None = Field(default=None, description="Corner radius seed in px, 0 (sharp) to 32 (very round); 24 is the default")
    font: Literal["Plus Jakarta Sans", "System", "Serif", "Mono"] | None = Field(
        default=None, description="Font category; with googleFont it is the fallback (Serif, Mono, else sans)"
    )
    googleFont: str | None = Field(
        default=None, description="Exact Google Fonts family name (e.g. Inter, Playfair Display), only if one is named or the site loads it"
    )
    rationale: str = Field(default="", description="One short phrase on the choice")


PLAN_SYSTEM = """You turn the styling words in an app request into design-system seed values.
Fill only the fields the request implies; leave the rest null. Colors are #rrggbb. Map named or
described colors ("terracotta", "forest green", "pastel") to a fitting hex. For a dark or light
request set mode. Rounded/soft means a large radius (24-32), sharp/square means 0-4. Pick Serif for
classic, editorial or elegant requests and Mono for technical or terminal-like ones. If the request
names a specific typeface, put its exact family name in googleFont and set font to its category; it is
checked against Google Fonts and dropped if Google does not serve it. Ignore anything that is not
about look and feel."""


def wants_theme(prompt: str) -> bool:
    from a2ui_apps.site_theme import find_url

    return bool(_HINT.search(prompt) or find_url(prompt))


SITE_SYSTEM = """When website evidence is given, the user wants that site's look: base every seed on the
evidence, not on taste. Primary: the first "brand color candidate" unless the request names another;
it must be a saturated color, never near-black, near-white or gray. Accent: a later candidate of a
clearly different hue, if any. Neutral: the most used mid gray. Mode: dark if the page background is
dark or the theme-color is a dark hint, light if they are light. Radius: from the control radii (999
or 50% means pill, use 32). Font: Serif if serif families dominate, Mono if monospace dominates the
UI (not just code), System for system-ui/-apple-system stacks, otherwise Plus Jakarta Sans.
googleFont: if the site loads Google Fonts, the one its body/UI text uses (prefer one that also
appears in the font families; skip icon fonts and code-only fonts), else null.
If evidence strength is weak, the candidates may be illustration colors: if you reliably know the
brand's own color, use it and say so in the rationale; otherwise pick the most brand-like candidate."""


def _hex(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()
    if not value.startswith("#"):
        value = "#" + value
    if not HEX.match(value):
        return None
    if len(value) == 4:  # #rgb -> #rrggbb
        value = "#" + "".join(c * 2 for c in value[1:])
    return value.lower()


# cre8 paints light-mode buttons with the primary seed itself, under white text.
MIN_TEXT_CONTRAST = 4.5  # WCAG AA for normal text


def _luminance(hex_color: str) -> float:
    def channel(c: int) -> float:
        v = c / 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4

    r, g, b = (int(hex_color[i : i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast_with_white(hex_color: str) -> float:
    return 1.05 / (_luminance(hex_color) + 0.05)


def readable_on_white_text(hex_color: str) -> str:
    """Darken (keeping hue) until white text on it meets WCAG AA; unchanged if it already does."""
    r, g, b = (int(hex_color[i : i + 2], 16) for i in (1, 3, 5))
    color = hex_color
    factor = 1.0
    while contrast_with_white(color) < MIN_TEXT_CONTRAST and factor > 0.05:
        factor *= 0.95
        color = "#{:02x}{:02x}{:02x}".format(*(round(c * factor) for c in (r, g, b)))
    return color


def normalize(spec: ThemeSpec) -> dict[str, Any]:
    """Validated seeds only; anything the agent got wrong is dropped, not passed on."""
    out: dict[str, Any] = {}
    if spec.mode in ("auto", "light", "dark"):
        out["mode"] = spec.mode
    for key in ("primary", "accent", "neutral"):
        if color := _hex(getattr(spec, key)):
            out[key] = color
    # Light (and auto) mode paints buttons with the seed itself under white text. Dark mode
    # uses a derived light shade under dark text, so darkening there only distorts the ramp.
    if "primary" in out and out.get("mode") != "dark":
        out["primary"] = readable_on_white_text(out["primary"])
    if isinstance(spec.radius, int):
        out["radius"] = max(0, min(32, spec.radius))
    if spec.font in FONTS:
        out["font"] = spec.font
    return out


def plan_theme(
    prompt: str, llm: LLM, evidence: str | None = None, fonts: GoogleFonts | None = None
) -> tuple[dict[str, Any], str] | None:
    """(seeds, rationale) if the prompt asks for a look, else None. No model call without a hint.

    `evidence` is a website's extracted design tokens (site_theme.SiteEvidence.summary()).
    `fonts` validates a googleFont choice; without it the choice is dropped.
    """
    if not wants_theme(prompt):
        return None
    system = [PLAN_SYSTEM, SITE_SYSTEM] if evidence else [PLAN_SYSTEM]
    request = f"{prompt}\n\n{evidence}" if evidence else prompt
    spec = llm.structured(task="theme.plan", system=system, prompt=request, schema=ThemeSpec, effort="low")
    seeds = normalize(spec)
    rationale = spec.rationale
    if spec.googleFont:
        family = " ".join(spec.googleFont.split())
        found = fonts.resolve(family) if fonts else None
        if found:
            seeds["googleFont"] = {"family": found[0], "weights": list(found[1])}
        else:
            rationale = f"{rationale}; {family!r} is not a Google font, kept the category".lstrip("; ")
    return (seeds, rationale) if seeds else None


def with_theme_extension(message: dict[str, Any], seeds: dict[str, Any]) -> dict[str, Any]:
    """Stamp the seeds onto a createSurface as metadata.extensions.cre8_theme."""
    body = message.get("createSurface")
    if not isinstance(body, dict):
        return message
    metadata = dict(body.get("metadata") or {})
    extensions = {**(metadata.get("extensions") or {}), EXTENSION_KEY: seeds}
    return {**message, "createSurface": {**body, "metadata": {**metadata, "extensions": extensions}}}
