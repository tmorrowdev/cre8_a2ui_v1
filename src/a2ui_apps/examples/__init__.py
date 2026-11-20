"""Few-shot examples for model-written UI.

Each `*.json` file is one example: a JSON array of A2UI v1.0 messages (a single
createSurface). Examples may use composites (`MetricCard`, `ChartCard`, ...):
those are gold-standard layouts that teach the model to compose from the
high-level catalog rather than stack primitives. `load_examples(validate=True)`
from a2ui-agent-sdk checks them against the inference catalog (cre8 plus
composites) in the test suite. Per request, `pick_examples` chooses the
examples closest to the selected components; the SDK prompt generator
decompiles them into whichever inference format is active.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

EXAMPLES_DIR = Path(__file__).parent


@lru_cache(maxsize=1)
def all_examples() -> dict[str, list[dict[str, Any]]]:
    return {p.stem: json.loads(p.read_text()) for p in sorted(EXAMPLES_DIR.glob("*.json"))}


def components_of(messages: list[dict[str, Any]]) -> set[str]:
    return {
        c["component"]
        for m in messages
        for key in ("createSurface", "updateComponents")
        for c in (m.get(key) or {}).get("components", [])
    }


def expanded(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """An example with every composite lowered to cre8 primitives (what the renderer would get)."""
    from a2ui.parser.messages import to_message_models

    from a2ui_apps.macros import expand
    from a2ui_apps.sdk import to_dicts

    return to_dicts(expand(to_message_models(messages)))


@lru_cache(maxsize=None)
def primitives_of(name: str) -> frozenset[str]:
    """The cre8 components an example renders with, composites expanded."""
    return frozenset(components_of(expanded(all_examples()[name])))


def pick_examples(selected: set[str], k: int = 1) -> list[list[dict[str, Any]]]:
    """The k examples whose components overlap the selection most (Jaccard).

    The selection names cre8 primitives, so an example is compared by what it
    renders with: a dashboard written with `KpiRow`/`ChartCard` still matches a
    selection of Cre8Grid, Cre8Card and Cre8Chart.
    """
    scored = []
    for name, messages in all_examples().items():
        used = primitives_of(name) - {"Text"}
        overlap = len(used & selected) / len(used | selected) if used | selected else 0
        scored.append((overlap, name, messages))
    scored.sort(key=lambda t: (-t[0], t[1]))
    return [messages for overlap, _, messages in scored[:k] if overlap > 0]
