"""An offline LLM for demos and browser tests: canned, prompt-aware, deterministic."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

from a2ui_apps.pathways.dashboard import DashboardSlots
from a2ui_apps.pathways.form import FormSlots
from a2ui_apps.pathways.freeform import ComponentSelection
from a2ui_apps.router import RouteDecision
from a2ui_apps.theme import ThemeSpec

_DEMO_COLORS = {"green": "#16a34a", "terracotta": "#c2410c", "purple": "#7c3aed", "pink": "#db2777", "teal": "#0d9488", "orange": "#ea580c", "red": "#dc2626", "navy": "#1e3a8a"}


def _title(prompt: str, suffix: str) -> str:
    words = prompt.strip().rstrip(".").split()
    return (" ".join(words[:6]).capitalize() or "Untitled") + suffix


@dataclass
class DemoLLM:
    def structured(self, *, task, system, prompt, schema, effort="medium"):
        if schema is ThemeSpec:
            # Deterministic stand-in for the theme tool: hex codes and a few words.
            text = prompt.lower()
            hexes = re.findall(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b", prompt)
            named = next((v for k, v in _DEMO_COLORS.items() if k in text), None)
            return ThemeSpec(
                primary=hexes[0] if hexes else named,
                accent=hexes[1] if len(hexes) > 1 else None,
                mode="dark" if "dark" in text else ("light" if "light" in text else None),
                radius=32 if "round" in text else (2 if "square" in text or "sharp" in text else None),
                font="Serif" if "serif" in text and "sans" not in text else ("Mono" if "mono" in text else None),
                rationale="demo mode",
            )
        if schema is ComponentSelection:
            return ComponentSelection(components=["Cre8Card", "Cre8Badge", "Cre8List", "Cre8ListItem"])
        if schema is RouteDecision:
            return RouteDecision(pathway="freeform", confidence=0.9, reason="demo mode")
        if schema is FormSlots:
            return FormSlots(
                title=_title(prompt, ""),
                intro="Demo mode: these fields are canned, the pathway is real.",
                fields=[
                    {"name": "full_name", "label": "Full name", "kind": "text", "required": True},
                    {"name": "email", "label": "Email", "kind": "email", "required": True},
                    {"name": "plan", "label": "Plan", "kind": "select", "options": ["Starter", "Team", "Enterprise"]},
                    {"name": "notes", "label": "Notes", "kind": "text"},
                ],
                submit_label="Submit",
                success_message="Thanks! Your submission was received.",
            )
        if schema is DashboardSlots:
            return DashboardSlots(
                title=_title(prompt, ""),
                subtitle="Demo mode: sample data for the last 30 days.",
                metrics=[
                    {"label": "Revenue", "value": "$48.2k", "delta": "+6.1%", "trend": "up"},
                    {"label": "Orders", "value": "1,204", "delta": "+3.0%", "trend": "up"},
                    {"label": "Refund rate", "value": "1.9%", "delta": "+0.4%", "trend": "up", "good_when_up": False},
                    {"label": "Avg. order", "value": "$40.03", "trend": "flat"},
                ],
                sections=[
                    {
                        "title": "Top products",
                        "kind": "table",
                        "columns": ["Product", "Units", "Revenue"],
                        "rows": [["Ceramic mug", "320", "$6,400"], ["Linen apron", "210", "$8,190"], ["Tea set", "96", "$7,680"]],
                    },
                    {
                        "title": "Quarterly goals",
                        "kind": "progress",
                        "items": [{"label": "Revenue", "value": 62, "max": 100}, {"label": "New customers", "value": 81, "max": 100}],
                    },
                ],
            )
        raise NotImplementedError(f"DemoLLM has no canned {schema.__name__}")

    def text(self, *, task, system, messages, effort="medium"):
        """Express output, top-down, as the freeform pathway's prompt asks for."""
        edit = re.search(r'surface\("([^"]+)", update=true\)', "\n".join(system))
        if edit:
            # Canvas mode: change the demo button in place.
            request = messages[0]["content"].rsplit("Change request:", 1)[-1].strip().split("\n")[0][:40].replace('"', "'")
            return f"""Demo mode: relabelled the button.
<a2ui>
surface("{edit.group(1)}", update=true)
cta = Cre8Button(text="Edited: {request}", variant="primary", on_click=Event("ack"))
</a2ui>"""
        prompt = messages[0]["content"].split("\n\nViewer:", 1)[0]  # drop the renderer context line
        title = _title(prompt, "").replace('"', "'")
        return f"""Here is a demo layout for your request.
<a2ui>
root = Cre8LayoutSection(children=[body])
body = HtmlDiv(display="flex", direction="column", gap="16", children=[title, card, cta])
title = Cre8Heading(type="headline-large", tagVariant="h1", children=[Text(text="{title}")])
card = Cre8Card(slot_default=[HtmlDiv(display="flex", direction="column", gap="8", padding="16", children=[Cre8Badge(text="Demo", status="info"), Cre8TextPassage(children=[Text(text="Demo mode: the freeform pathway streams Express through the a2ui-agent-sdk parser.")])])])
cta = Cre8Button(text="Got it", variant="secondary", on_click=Event("ack"))
</a2ui>"""

    def stream_text(self, *, task, system, messages, effort="medium"):
        text = self.text(task=task, system=system, messages=messages, effort=effort)
        for i in range(0, len(text), 29):
            yield text[i : i + 29]
