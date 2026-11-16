"""Choose a pathway: deterministic rules first, the model only when they are ambiguous."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, Field

from a2ui_apps.llm import LLM
from a2ui_apps.pathways.base import Pathway

MIN_CONFIDENCE = 0.5


class RouteDecision(BaseModel):
    pathway: Literal["form", "dashboard", "freeform"]
    confidence: float = Field(description="0 to 1")
    reason: str


@dataclass(frozen=True)
class Route:
    pathway: str
    source: Literal["rules", "model", "fallback"]
    reason: str
    matches: dict[str, list[str]]


def keyword_matches(prompt: str, pathways: dict[str, Pathway]) -> dict[str, list[str]]:
    text = prompt.lower()
    found: dict[str, list[str]] = {}
    for name, pathway in pathways.items():
        hits = [k for k in pathway.keywords if re.search(rf"\b{re.escape(k)}\b", text)]
        if hits:
            found[name] = hits
    return found


def route(prompt: str, pathways: dict[str, Pathway], llm: LLM) -> Route:
    matches = keyword_matches(prompt, pathways)
    if len(matches) == 1:
        (name, hits), = matches.items()
        return Route(name, "rules", f"matched {', '.join(hits)}", matches)

    menu = "\n".join(f"- {name}: {p.description}" for name, p in pathways.items())
    decision = llm.structured(
        task="route",
        system=[f"Pick the pathway that best builds the requested app.\n{menu}"],
        prompt=prompt,
        schema=RouteDecision,
        effort="low",
    )
    if decision.pathway not in pathways or decision.confidence < MIN_CONFIDENCE:
        return Route("freeform", "fallback", f"model chose {decision.pathway} at {decision.confidence:.2f}", matches)
    return Route(decision.pathway, "model", decision.reason, matches)
