"""Google Fonts in the theme: detection on a site, validation against the API, delivery as a seed."""

from __future__ import annotations

import httpx

from a2ui_apps.engine import Engine
from a2ui_apps.google_fonts import GoogleFonts, css_url, families_in_urls
from a2ui_apps.llm import ScriptedLLM
from a2ui_apps.site_theme import site_evidence
from a2ui_apps.theme import plan_theme

SERVED = "@font-face { font-family: 'X'; src: url(https://fonts.gstatic.com/s/x/v1/a.ttf) format('truetype'); }"
ALIAS = "@font-face { font-family: 'X'; src: url(https://fonts.gstatic.com/l/font?kit=abc) format('truetype'); }"


class FakeApi:
    """Families mapped to the weight sets the API accepts; anything else is a 400."""

    def __init__(self, families: dict[str, set[tuple[int, ...]] | str]):
        self.families = families
        self.urls: list[str] = []

    def __call__(self, url: str) -> tuple[int, str]:
        self.urls.append(url)
        for family, accepted in self.families.items():
            for weights in ({(400, 500, 600, 700), (400, 700), (400,)} if accepted in ("all", "alias") else accepted):
                if url == css_url(family, weights):
                    return 200, ALIAS if accepted == "alias" else SERVED
        return 400, "Bad Request"


def test_finds_families_in_css2_and_css_v1_urls():
    text = (
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&amp;family=Playfair+Display:ital@1&display=swap">'
        " @import url(https://fonts.googleapis.com/css?family=Lato:400,700|Roboto+Mono);"
        ' <link href="https://example.com/css?family=Nope">'
    )
    assert families_in_urls(text) == ["Inter", "Playfair Display", "Lato", "Roboto Mono"]


def test_resolve_picks_the_widest_weight_set_and_caches():
    api = FakeApi({"Lobster": {(400,)}, "Inter": "all"})
    fonts = GoogleFonts(api)
    assert fonts.resolve("Lobster") == ("Lobster", (400,))
    assert fonts.resolve("Inter") == ("Inter", (400, 500, 600, 700))
    calls = len(api.urls)
    fonts.resolve("Lobster")
    assert len(api.urls) == calls


def test_resolve_retries_in_title_case_but_tries_the_exact_name_first():
    fonts = GoogleFonts(FakeApi({"Playfair Display": "all", "IBM Plex Sans": "all"}))
    assert fonts.resolve("playfair  display") == ("Playfair Display", (400, 500, 600, 700))
    assert fonts.resolve("IBM Plex Sans")[0] == "IBM Plex Sans"


def test_rejects_unknown_system_alias_and_malformed_names():
    api = FakeApi({"Helvetica": "alias"})
    fonts = GoogleFonts(api)
    assert fonts.resolve("Helvetica") is None  # served from /l/: a look-alike, not the font
    assert fonts.resolve("Definitely Not A Font") is None
    before = len(api.urls)
    for bad in ("Inter; } body { color: red", "Inter&family=Evil", "x", "A" * 80):
        assert fonts.resolve(bad) is None
    assert len(api.urls) == before  # malformed names never reach the network


def test_offline_is_not_cached_as_invalid():
    state = {"offline": True}

    def probe(url):
        if state["offline"]:
            raise httpx.ConnectError("offline")
        return 200, SERVED

    fonts = GoogleFonts(probe)
    assert fonts.resolve("Inter") is None
    state["offline"] = False
    assert fonts.resolve("Inter") == ("Inter", (400, 500, 600, 700))


def test_plan_theme_delivers_a_validated_google_font():
    fonts = GoogleFonts(FakeApi({"Playfair Display": {(400, 700)}}))
    llm = ScriptedLLM({"theme.plan": [{"font": "Serif", "googleFont": "Playfair Display"}]})
    seeds, _ = plan_theme("An editorial blog in Playfair Display font", llm, fonts=fonts)
    assert seeds == {"font": "Serif", "googleFont": {"family": "Playfair Display", "weights": [400, 700]}}


def test_plan_theme_drops_a_font_google_does_not_serve():
    fonts = GoogleFonts(FakeApi({}))
    llm = ScriptedLLM({"theme.plan": [{"font": "System", "googleFont": "Helvetica"}]})
    seeds, rationale = plan_theme("Use the Helvetica font", llm, fonts=fonts)
    assert seeds == {"font": "System"} and "not a Google font" in rationale


HTML = """<!doctype html><html><head><title>Acme</title>
<link rel="preconnect" href="https://fonts.gstatic.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;700&display=swap" rel="stylesheet">
<style>body { font-family: 'DM Sans', sans-serif; background: #ffffff; }</style>
</head><body><button style="background:#7c3aed">Go</button></body></html>"""


def test_site_google_fonts_reach_the_theme_tool():
    def fetch(url, limit):
        return "https://acme.example/", HTML

    evidence = site_evidence("https://acme.example/", fetch)
    assert evidence.google_fonts == ["DM Sans"] and evidence.stylesheets_read == 0  # not fetched as a stylesheet
    assert "Google Fonts loaded by the site: DM Sans" in evidence.summary()

    form = {"title": "Order", "intro": "Hi.", "submit_label": "Send", "success_message": "Thanks",
            "fields": [{"name": "email", "label": "Email", "kind": "email"}]}
    llm = ScriptedLLM({"theme.plan": [{"primary": "#7c3aed", "googleFont": "DM Sans"}], "form.plan": [form]})
    engine = Engine(llm, fetch=fetch, fonts=GoogleFonts(FakeApi({"DM Sans": "all"})))
    events = list(engine.stream("An order form styled like https://acme.example"))
    site = next(e["step"] for e in events if e.get("step", {}).get("name") == "site")
    assert "Google Fonts DM Sans" in site["detail"]
    theme = next(e["theme"] for e in events if "theme" in e)
    assert theme["googleFont"] == {"family": "DM Sans", "weights": [400, 500, 600, 700]}
