"""Composite components: the catalog layer the runtime agent composes from.

Each composite is a `@macro` function in its own module here. The runtime
agent sees them as ordinary catalog components (`MetricCard(...)`,
`ChartCard(...)`), and `a2ui_apps.macros.expand` lowers them to cre8
primitives before anything reaches the renderer.

This package is the seam between the two halves of the hybrid setup:

- Build time: people, or the catalog-authoring agent
  (`scripts/author_composite.py`), add a module here plus a few-shot example
  in `a2ui_apps/examples/`. `tests/test_composites.py` checks every module.
- Runtime: `discover()` collects every composite, so a new module is in the
  prompt, the parser and the expander with no other registration.

Rules for a composite module (the authoring agent is held to the same ones):

- exactly one `@macro` function, PascalCase, not a name the catalog already has;
- a Google-style docstring with an `Args:` line per parameter (that text is
  what the model reads);
- build only from `a2ui_apps.builders.cre8` and `a2ui.builder.v1_0`;
- styling stays in the renderer: use the token-valued props (gap, padding,
  heading `type`, button `variant`, badge `status`), never colors or CSS.
"""

from __future__ import annotations

import importlib
import pkgutil
from collections.abc import Callable
from functools import lru_cache
from types import ModuleType
from typing import Any

Macro = Callable[..., Any]


def is_macro(obj: Any) -> bool:
    return callable(obj) and hasattr(obj, "__a2ui_macro__")


def macro_name(obj: Macro) -> str:
    """The component name the model sees (the macro's PascalCase name)."""
    return obj.__a2ui_macro__.name


def macros_in(module: ModuleType) -> list[Macro]:
    """The macros a module defines itself (not ones it imports)."""
    return [v for v in vars(module).values() if is_macro(v) and getattr(v, "__module__", None) == module.__name__]


@lru_cache(maxsize=1)
def discover() -> tuple[Macro, ...]:
    """Every composite in this package, in module-name order."""
    found: list[Macro] = []
    for info in sorted(pkgutil.iter_modules(__path__), key=lambda i: i.name):
        if info.name.startswith("_"):
            continue
        found.extend(macros_in(importlib.import_module(f"{__name__}.{info.name}")))
    return tuple(found)
