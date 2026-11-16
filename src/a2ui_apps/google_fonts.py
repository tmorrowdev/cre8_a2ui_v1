"""Google Fonts: detect them on a site, validate a family exists, and pick loadable weights.

Validation asks the Google Fonts CSS API itself (fonts.googleapis.com/css2), which
answers 400 for a family it does not serve. The renderer builds the stylesheet URL
from the validated family and weights; it never loads a URL taken from model output.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from urllib.parse import parse_qs, unquote_plus, urlparse

import httpx

CSS_API = "https://fonts.googleapis.com/css2"
FAMILY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ]{0,58}[A-Za-z0-9]$")
WEIGHT_SETS = ((400, 500, 600, 700), (400, 700), (400,))
# A real Google Fonts family is served from gstatic /s/<family>/. For system-font names
# (Helvetica, Georgia, Times, Verdana...) the API answers 200 with a substitute from /l/,
# which would silently swap the site's font for a look-alike, so those are rejected.
_SERVED = re.compile(r"url\(https://fonts\.gstatic\.com/s/")
_GOOGLE_URL = re.compile(r"https?://fonts\.googleapis\.com/css2?\?[^\s\"')<>]+", re.IGNORECASE)

Probe = Callable[[str], tuple[int, str]]


def _http_probe(url: str) -> tuple[int, str]:
    response = httpx.get(url, timeout=4.0, headers={"User-Agent": "a2ui-apps-font-check/0.1"})
    return response.status_code, response.text[:2000]


def css_url(family: str, weights: tuple[int, ...] | list[int]) -> str:
    return f"{CSS_API}?family={family.replace(' ', '+')}:wght@{';'.join(map(str, weights))}&display=swap"


def families_in_urls(text: str) -> list[str]:
    """Family names from fonts.googleapis.com links or @imports (css and css2 APIs)."""
    found: list[str] = []
    for url in _GOOGLE_URL.findall(text.replace("&amp;", "&")):
        for value in parse_qs(urlparse(url).query).get("family", []):
            for part in unquote_plus(value).split("|"):  # css v1 joins families with |
                name = part.split(":")[0].strip()
                if name and name not in found:
                    found.append(name)
    return found


class GoogleFonts:
    """Validates family names against the Google Fonts API, with a cache."""

    def __init__(self, probe: Probe | None = None) -> None:
        self.probe = probe or _http_probe
        self._cache: dict[str, tuple[int, ...] | None] = {}

    def resolve(self, family: str) -> tuple[str, tuple[int, ...]] | None:
        """(canonical family, weights) if Google Fonts serves it, else None.

        The API is case-sensitive ("inter" is a 400), so a miss is retried in title case;
        exact spelling is tried first so names like "IBM Plex Sans" survive."""
        name = " ".join(family.split())
        for candidate in dict.fromkeys((name, name.title())):
            if weights := self.weights(candidate):
                return candidate, weights
        return None

    def weights(self, family: str) -> tuple[int, ...] | None:
        """The weight set the API serves for this exact family name, or None."""
        name = " ".join(family.split())
        if not FAMILY.match(name):
            return None
        key = name
        if key in self._cache:
            return self._cache[key]
        result: tuple[int, ...] | None = None
        for weights in WEIGHT_SETS:
            try:
                status, body = self.probe(css_url(name, weights))
            except httpx.HTTPError:
                return None  # offline: unknown rather than invalid, so not cached
            if status == 200:
                result = weights if _SERVED.search(body) else None
                break
            if status != 400:  # 400 = unknown family or unavailable weight; try fewer
                return None
        self._cache[key] = result
        return result
