"""cre8 macros: composite components the model can use, lowered to cre8 primitives.

The composites themselves live one per module in `a2ui_apps.composites`
(that is where the build-time authoring agent adds new ones). This module is
the runtime side: the model sees every composite as an ordinary catalog
component (the expander adds their schemas to the inference catalog), so one
`MetricCard(...)` line replaces a dozen nested components. Before anything
reaches the renderer or the agent's state, `expand` lowers every macro into
cre8 primitives, so the browser only ever needs the cre8 catalog.
"""

from __future__ import annotations

from collections.abc import Sequence
from functools import lru_cache
from typing import Any

from a2ui.transformers.macros import MacroExpander

from a2ui_apps.composites import Macro, discover, macro_name
from a2ui_apps.validate import load_catalog

MACROS: list[Macro] = list(discover())


def build_expander(macros: Sequence[Macro]) -> MacroExpander:
    """An expander over the cre8 catalog. Raises on a bad invocation, so repair loops see the error."""
    return MacroExpander(list(macros), base_catalogs=[load_catalog().api], protocol_version="1.0", on_error="raise")


@lru_cache(maxsize=1)
def expander() -> MacroExpander:
    return build_expander(MACROS)


@lru_cache(maxsize=1)
def inference_catalog() -> Any:
    """The cre8 catalog plus macro components: what the prompt and parser see."""
    return expander().transform_to_inference_catalog(load_catalog().api)


def macro_names() -> list[str]:
    return [macro_name(m) for m in MACROS]


def expand(messages: Sequence[Any]) -> list[Any]:
    """Lower macro components to cre8 primitives (models or dicts in, as the SDK returns)."""
    return list(expander().transform_to_transport(list(messages)))
