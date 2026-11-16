"""Theme evidence from a website: fetch it safely, extract its design tokens.

When a prompt names a site ("match the look of stripe.com"), the theme tool
gets facts instead of guesses. Everything here is deterministic; the model
only chooses seeds from the evidence (see theme.py).

Fetching user-supplied URLs from a server is an SSRF risk, so `SafeFetcher`
allows only http(s), resolves every host and refuses private, loopback,
link-local, multicast and reserved addresses (cloud metadata included),
re-checks every redirect, and caps time, size and the number of requests.
This copies design tokens (colors, font category, corner radius, light/dark),
not a site's logos, images or layout.
"""

from __future__ import annotations

import ipaddress
import re
import socket
from collections import Counter
from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import Callable, Protocol
from urllib.parse import urljoin, urlparse

import httpx

from a2ui_apps.google_fonts import families_in_urls

MAX_HTML = 1_500_000
MAX_CSS = 1_000_000
MAX_STYLESHEETS = 5
TIMEOUT = 6.0
MAX_REDIRECTS = 3
USER_AGENT = "a2ui-apps-theme-fetcher/0.1"

_URL = re.compile(r"\bhttps?://[^\s<>\"')]+", re.IGNORECASE)
_DOMAIN = re.compile(
    r"\b(?:[a-z0-9-]+\.)+(?:com|org|net|io|dev|app|ai|co|design|studio|shop|store|tech|xyz|me|so|gg|edu|gov|uk|de|fr|ca|au)\b(?:/[^\s]*)?",
    re.IGNORECASE,
)


class BlockedURL(ValueError):
    """The URL is not allowed (scheme, host or resolved address)."""


def find_url(prompt: str) -> str | None:
    """An explicit http(s) URL, or a bare domain such as stripe.com."""
    if match := _URL.search(prompt):
        return match.group(0).rstrip(".,;:!?")
    if match := _DOMAIN.search(prompt):
        return "https://" + match.group(0).rstrip(".,;:!?")
    return None


def _check_address(ip: str) -> None:
    addr = ipaddress.ip_address(ip)
    if (
        addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_multicast
        or addr.is_reserved or addr.is_unspecified or (addr.version == 6 and addr.ipv4_mapped is not None and not addr.ipv4_mapped.is_global)
        or not addr.is_global
    ):
        raise BlockedURL(f"address {ip} is not public")


def check_url(url: str, resolve: Callable[[str], list[str]] | None = None) -> None:
    """Raise BlockedURL unless every address the host resolves to is public."""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise BlockedURL(f"scheme {parsed.scheme!r} is not allowed")
    if not parsed.hostname:
        raise BlockedURL("no host")
    if parsed.username or parsed.password:
        raise BlockedURL("credentials in URLs are not allowed")
    host = parsed.hostname
    try:
        _check_address(host)  # a literal IP
        return
    except ValueError as e:
        if isinstance(e, BlockedURL):
            raise
    addresses = (resolve or _resolve)(host)
    if not addresses:
        raise BlockedURL(f"{host} does not resolve")
    for ip in addresses:
        _check_address(ip)


def _resolve(host: str) -> list[str]:
    try:
        return sorted({info[4][0] for info in socket.getaddrinfo(host, None)})
    except socket.gaierror:
        return []


class Fetcher(Protocol):
    def __call__(self, url: str, limit: int) -> tuple[str, str]: ...


class SafeFetcher:
    """GET with SSRF checks on the URL and every redirect. Returns (final_url, text)."""

    def __init__(self, resolve: Callable[[str], list[str]] | None = None, transport: httpx.BaseTransport | None = None) -> None:
        self.resolve = resolve
        self.transport = transport  # tests inject a MockTransport

    def __call__(self, url: str, limit: int) -> tuple[str, str]:
        with httpx.Client(
            timeout=TIMEOUT, follow_redirects=False, headers={"User-Agent": USER_AGENT}, transport=self.transport
        ) as client:
            for _ in range(MAX_REDIRECTS + 1):
                check_url(url, self.resolve)
                with client.stream("GET", url) as response:
                    if response.is_redirect:
                        url = urljoin(url, response.headers.get("location", ""))
                        continue
                    response.raise_for_status()
                    chunks, size = [], 0
                    for chunk in response.iter_bytes():
                        size += len(chunk)
                        if size > limit:
                            break
                        chunks.append(chunk)
                    return str(response.url), b"".join(chunks).decode(response.encoding or "utf-8", errors="replace")
        raise BlockedURL("too many redirects")


class _PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.stylesheets: list[str] = []
        self.inline_css: list[str] = []
        self.theme_color: str | None = None
        self.google_links: list[str] = []
        self.title = ""
        self._in_style = self._in_title = False
        # Page outline for layout cues: headings, nav labels, call-to-action labels.
        self.description = ""
        self.site_name = ""
        self.headings: list[str] = []
        self.nav: list[str] = []
        self.actions: list[str] = []
        self._captures: list[tuple[str, str, list[str]]] = []  # (tag, kind, text parts)
        self._nav_depth = 0
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "link" and "fonts.googleapis.com" in a.get("href", ""):
            self.google_links.append(a["href"])
        elif tag == "link" and "stylesheet" in a.get("rel", "").lower() and a.get("href"):
            self.stylesheets.append(a["href"])
        elif tag == "meta" and a.get("name", "").lower() == "theme-color":
            self.theme_color = a.get("content") or None
        elif tag == "meta" and (a.get("name", "").lower() == "description" or a.get("property", "") == "og:description"):
            self.description = self.description or _clean(a.get("content", ""), 200)
        elif tag == "meta" and a.get("property", "") == "og:site_name":
            self.site_name = _clean(a.get("content", ""), 60)
        elif tag == "style":
            self._in_style = True
        elif tag == "title":
            self._in_title = True
        if a.get("style"):
            self.inline_css.append(f"x{{{a['style']}}}")
        if tag in _SKIP:
            self._skip_depth += 1
        elif tag in ("nav", "header"):
            self._nav_depth += 1
        elif tag in ("h1", "h2", "h3"):
            self._captures.append((tag, "heading", []))
        elif tag == "button" or (tag == "a" and _CTA.search(a.get("class", "") + " " + a.get("role", ""))):
            self._captures.append((tag, "action", []))
        elif tag == "a" and self._nav_depth:
            self._captures.append((tag, "nav", []))

    def handle_endtag(self, tag):
        if tag == "style":
            self._in_style = False
        elif tag == "title":
            self._in_title = False
        if tag in _SKIP:
            self._skip_depth = max(0, self._skip_depth - 1)
        elif tag in ("nav", "header"):
            self._nav_depth = max(0, self._nav_depth - 1)
        for i in range(len(self._captures) - 1, -1, -1):
            if self._captures[i][0] == tag:
                _, kind, parts = self._captures.pop(i)
                text = _clean(" ".join(parts), 90)
                target, cap = {"heading": (self.headings, 14), "nav": (self.nav, 14), "action": (self.actions, 10)}[kind]
                if text and text not in target and len(target) < cap:
                    target.append(text)
                break

    def handle_data(self, data):
        if self._in_style:
            self.inline_css.append(data)
        elif self._in_title:
            self.title += data
        elif not self._skip_depth:
            for _, _, parts in self._captures:
                parts.append(data)


_SKIP = {"script", "noscript", "svg", "template"}
_CTA = re.compile(r"(\bbtn|button|cta)", re.IGNORECASE)


def _clean(text: str, limit: int) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


_COLOR = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b|rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+(?:\s*,\s*[\d.]+)?\s*\)")
_RULE = re.compile(r"([^{}]+)\{([^{}]*)\}")
_DECL = re.compile(r"([\w-]+)\s*:\s*([^;]+)")
_BRAND_VAR = re.compile(r"(primary|brand|accent|link|cta|highlight)", re.IGNORECASE)
_BUTTONISH = re.compile(r"(button|\bbtn|\.cta|primary|\ba\b|\ba:|link)", re.IGNORECASE)


def to_hex(value: str) -> str | None:
    value = value.strip().lower()
    if value.startswith("#"):
        if len(value) == 4:
            return "#" + "".join(c * 2 for c in value[1:])
        return value if len(value) == 7 else None
    m = re.match(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*([\d.]+))?", value)
    if not m:
        return None
    if m.group(4) is not None and float(m.group(4)) < 0.5:
        return None  # mostly transparent: not a brand color
    r, g, b = (min(255, int(x)) for x in m.groups()[:3])
    return f"#{r:02x}{g:02x}{b:02x}"


def _saturation_and_lightness(hex_color: str) -> tuple[float, float]:
    r, g, b = (int(hex_color[i : i + 2], 16) / 255 for i in (1, 3, 5))
    hi, lo = max(r, g, b), min(r, g, b)
    light = (hi + lo) / 2
    sat = 0.0 if hi == lo else (hi - lo) / (1 - abs(2 * light - 1))
    return sat, light


@dataclass
class SiteEvidence:
    url: str
    title: str = ""
    theme_color: str | None = None
    brand_vars: dict[str, str] = field(default_factory=dict)
    button_colors: list[str] = field(default_factory=list)
    saturated: list[tuple[str, int]] = field(default_factory=list)
    neutrals: list[tuple[str, int]] = field(default_factory=list)
    fonts: list[tuple[str, int]] = field(default_factory=list)
    radii_px: list[tuple[int, int]] = field(default_factory=list)
    google_fonts: list[str] = field(default_factory=list)
    description: str = ""
    site_name: str = ""
    headings: list[str] = field(default_factory=list)
    nav: list[str] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)

    def outline(self) -> str:
        """The page's own words, for layout cues: what sections and actions it has."""
        lines = [f"Website read: {self.url}" + (f" ({_clean(self.title, 80)})" if self.title.strip() else "")]
        if self.site_name:
            lines.append(f"- site name: {self.site_name}")
        if self.description:
            lines.append(f"- description: {self.description}")
        if self.nav:
            lines.append("- navigation: " + " | ".join(self.nav))
        if self.headings:
            lines.append("- headings, in page order: " + " | ".join(self.headings))
        if self.actions:
            lines.append("- buttons / calls to action: " + " | ".join(self.actions))
        return "\n".join(lines)
    page_background: str | None = None
    stylesheets_read: int = 0

    def brand_candidates(self, limit: int = 4) -> list[str]:
        """Saturated colors most likely to be the brand, best first (deterministic ranking).

        meta theme-color is only the browser-chrome color, often near-black, so it ranks
        only when saturated. Brand-named variables beat button colors beat raw frequency;
        among variables, names saying primary/brand and mid shades (400-700) come first.
        """
        def usable(color: str | None) -> bool:
            if not color or not color.startswith("#") or len(color) != 7:
                return False
            sat, light = _saturation_and_lightness(color)
            return sat > 0.35 and 0.18 < light < 0.82

        def var_rank(name: str) -> tuple[int, int, int]:
            shade = re.search(r"(\d{2,3})$", name)
            # Ramps name their brand step 500-600; prefer the shade closest to it.
            distance = abs(int(shade.group(1)) - 550) if shade else 300
            washed = 1 if re.search(r"disabled|muted|subtle|faded|inactive", name) else 0
            return (washed, 0 if re.search(r"primary|brand", name) else 1, distance)

        ranked: list[str] = []
        sources = [
            [c for _, c in sorted(((var_rank(n), c) for n, c in self.brand_vars.items()), key=lambda t: t[0])],
            self.button_colors,
            [self.theme_color] if self.theme_color else [],
            [c for c, _ in self.saturated],
        ]
        for source in sources:
            for color in source:
                if usable(color) and color not in ranked:
                    ranked.append(color)
        return ranked[:limit]

    def strength(self) -> str:
        """'strong' when the site names or repeats its brand color; 'weak' when colors are incidental."""
        named = any(re.search(r"primary|brand", n) for n in self.brand_vars)
        repeated = bool(self.saturated) and self.saturated[0][1] >= 5
        return "strong" if named or self.button_colors and repeated or repeated else "weak"

    def summary(self) -> str:
        lines = [f"Website: {self.url}" + (f" ({self.title.strip()[:80]})" if self.title.strip() else "")]
        lines.append(f"- evidence strength: {self.strength()}" + (
            " (no brand-named colors and nothing repeats; the brand color is probably set by scripts)" if self.strength() == "weak" else ""
        ))
        if candidates := self.brand_candidates():
            lines.append("- brand color candidates, best first: " + ", ".join(candidates))
        if self.theme_color:
            sat, light = _saturation_and_lightness(self.theme_color) if self.theme_color.startswith("#") and len(self.theme_color) == 7 else (1.0, 0.5)
            note = f" (neutral browser-chrome color: a {'dark' if light < 0.5 else 'light'} hint, not a brand color)" if sat < 0.2 else ""
            lines.append(f"- meta theme-color: {self.theme_color}{note}")
        if self.brand_vars:
            lines.append("- brand-named CSS variables: " + ", ".join(f"{k}={v}" for k, v in list(self.brand_vars.items())[:10]))
        if self.button_colors:
            lines.append("- button/link colors: " + ", ".join(self.button_colors[:8]))
        if self.saturated:
            lines.append("- most used saturated colors: " + ", ".join(f"{c} x{n}" for c, n in self.saturated[:8]))
        if self.neutrals:
            lines.append("- most used neutrals: " + ", ".join(f"{c} x{n}" for c, n in self.neutrals[:6]))
        if self.google_fonts:
            lines.append("- Google Fonts loaded by the site: " + ", ".join(self.google_fonts[:4]))
        if self.fonts:
            lines.append("- font families: " + ", ".join(f"{f} x{n}" for f, n in self.fonts[:6]))
        if self.radii_px:
            lines.append("- button/control corner radii (px): " + ", ".join(f"{r} x{n}" for r, n in self.radii_px[:6]))
        if self.page_background:
            lines.append(f"- page background: {self.page_background}")
        return "\n".join(lines)


def extract(url: str, html: str, stylesheets: list[str]) -> SiteEvidence:
    parser = _PageParser()
    parser.feed(html)
    evidence = SiteEvidence(
        url=url, title=parser.title, theme_color=to_hex(parser.theme_color or "") or parser.theme_color,
        description=parser.description, site_name=parser.site_name,
        headings=parser.headings, nav=parser.nav, actions=parser.actions,
    )
    css = "\n".join([*parser.inline_css, *stylesheets])
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    colors: Counter[str] = Counter()
    fonts: Counter[str] = Counter()
    radii: Counter[int] = Counter()
    for selectors, body in _RULE.findall(css):
        buttonish = bool(_BUTTONISH.search(selectors))
        is_page = bool(re.search(r"(^|[\s,])(html|body|:root)\b", selectors))
        for prop, value in _DECL.findall(body):
            prop = prop.lower()
            if prop.startswith("--") and _BRAND_VAR.search(prop):
                if (c := to_hex(_COLOR.search(value).group(0)) if _COLOR.search(value) else None):
                    evidence.brand_vars.setdefault(prop, c)
            for raw in _COLOR.findall(value):
                if c := to_hex(raw):
                    colors[c] += 1
                    if buttonish and prop in ("background", "background-color", "color", "border-color"):
                        if c not in evidence.button_colors:
                            evidence.button_colors.append(c)
            if prop == "font-family":
                family = value.split(",")[0].strip().strip("'\"")
                if family and not family.startswith("var("):
                    fonts[family] += 1
                generic = value.lower()
                for kind in ("monospace", "serif"):
                    if re.search(rf"(^|,|\s){kind}\b", generic) and "sans-serif" not in generic.split(",")[-1]:
                        fonts[f"<{kind}>"] += 1
            if prop == "border-radius" and buttonish:
                if m := re.match(r"\s*(\d+(?:\.\d+)?)px", value):
                    radii[int(float(m.group(1)))] += 1
                elif re.match(r"\s*(9999|999|50%|100%)", value):
                    radii[999] += 1
            if is_page and prop in ("background", "background-color") and not evidence.page_background:
                if m := _COLOR.search(value):
                    evidence.page_background = to_hex(m.group(0))
    for color, count in colors.most_common(60):
        sat, light = _saturation_and_lightness(color)
        if sat > 0.35 and 0.15 < light < 0.85:
            evidence.saturated.append((color, count))
        elif sat < 0.15:
            evidence.neutrals.append((color, count))
    evidence.fonts = fonts.most_common(8)
    evidence.google_fonts = families_in_urls("\n".join([*parser.google_links, css]))
    evidence.radii_px = radii.most_common(6)
    evidence.stylesheets_read = len(stylesheets)
    return evidence


def site_evidence(url: str, fetch: Fetcher | None = None) -> SiteEvidence:
    """Fetch a page and up to MAX_STYLESHEETS of its stylesheets; extract design tokens."""
    fetch = fetch or SafeFetcher()
    final_url, html = fetch(url, MAX_HTML)
    parser = _PageParser()
    parser.feed(html)
    sheets: list[str] = []
    for href in parser.stylesheets[:MAX_STYLESHEETS]:
        try:
            sheets.append(fetch(urljoin(final_url, href), MAX_CSS)[1])
        except Exception:  # one bad stylesheet should not lose the rest
            continue
    return extract(final_url, html, sheets)
