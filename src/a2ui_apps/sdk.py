"""a2ui-agent-sdk wiring: catalogs, inference formats, request processors, state.

The SDK is model-agnostic: it builds the prompt, parses what the model writes
(Express by default, streaming) and validates every message against a
RendererState. This module binds it to the cre8 catalog; pathways call Claude.
"""

from __future__ import annotations

import os
from collections.abc import Callable, Sequence
from functools import lru_cache
from typing import Any

os.environ.setdefault("A2UI_SUPPRESS_EXPERIMENTAL_FEATURE_WARNINGS", "1")

from a2ui.catalog_transformers.pruning import ComponentPruningTransformer  # noqa: E402
from a2ui.core.exceptions import A2uiError  # noqa: E402
from a2ui.inference_formats.direct_json.format import DirectJsonFormatFactory  # noqa: E402
from a2ui.inference_formats.experimental.atom.format import AtomFormatFactory  # noqa: E402
from a2ui.inference_formats.experimental.elemental.format import ElementalFormatFactory  # noqa: E402
from a2ui.inference_formats.express.format import ExpressFormatFactory  # noqa: E402
from a2ui.processor.catalog_config import CatalogConfig  # noqa: E402
from a2ui.processor.generator import A2uiGenerator  # noqa: E402
from a2ui.processor.processor import A2uiRequestProcessor  # noqa: E402
from a2ui.utils.renderer_state import RendererState  # noqa: E402

from a2ui_apps.validate import load_catalog, unknown_property_errors  # noqa: E402

Message = dict[str, Any]

# What the model may emit when generating a fresh app. No deleteSurface, no RPC:
# the host owns surface lifecycle. Also prunes those rules out of the prompt.
GENERATION_MESSAGES = ("createSurface", "updateComponents", "updateDataModel")
EDIT_MESSAGES = ("updateComponents", "updateDataModel")


def _express(allowed: Sequence[str], surface_id: str):
    return ExpressFormatFactory(allowed_messages=list(allowed), surface_id=surface_id)


def _direct_json(allowed: Sequence[str], surface_id: str):
    # Direct JSON carries the surface id inside each message, so it has no default.
    return DirectJsonFormatFactory(allowed_messages=list(allowed), progressive_keys={"text"})


def _elemental(allowed: Sequence[str], surface_id: str):
    return ElementalFormatFactory(allowed_messages=list(allowed), surface_id=surface_id)


def _atom(allowed: Sequence[str], surface_id: str):
    return AtomFormatFactory(allowed_messages=list(allowed), surface_id=surface_id)


FORMATS: dict[str, Callable[[Sequence[str], str], Any]] = {
    "express": _express,
    "direct_json": _direct_json,
    "elemental": _elemental,  # experimental
    "atom": _atom,  # experimental
}
DEFAULT_FORMAT = os.environ.get("A2UI_APPS_FORMAT", "express")


def catalog_id() -> str:
    return load_catalog().catalog_id


def capabilities() -> dict[str, Any]:
    """What a cre8 renderer advertises; web_core's getRendererCapabilities has this shape."""
    return {"1.0": {"supportedCatalogIds": [catalog_id()]}}


def make_processor(
    *,
    surface_id: str,
    fmt: str = DEFAULT_FORMAT,
    allowed_messages: Sequence[str] = GENERATION_MESSAGES,
    components: Sequence[str] | None = None,
    examples: Sequence[Sequence[Message]] | None = None,
    renderer_capabilities: dict[str, Any] | None = None,
    state: RendererState | None = None,
) -> A2uiRequestProcessor:
    """A per-request processor: negotiated catalogs, a format, and a prompt.

    `components` prunes the catalog to an allowlist (Text is always kept), which
    is what keeps the generated prompt small enough to use.
    """
    if fmt not in FORMATS:
        raise ValueError(f"unknown inference format {fmt!r}; choose from {sorted(FORMATS)}")
    from a2ui_apps.macros import inference_catalog, macro_names

    transformers = []
    if components:
        # Macros are compact and broadly useful, so they survive every pruning.
        transformers.append(ComponentPruningTransformer(sorted({*components, "Text", *macro_names()})))
    config = CatalogConfig(inference_catalog(), transformers or None)
    generator = A2uiGenerator([config], examples=examples)
    return generator.create_processor(
        renderer_capabilities or capabilities(),
        FORMATS[fmt](allowed_messages, surface_id),
        state=state,
    )


def error_detail(error: Exception, code: str | None = None) -> dict[str, Any]:
    """An SDK/core exception in the renderer error-envelope shape the repair loop reads."""
    help_message = getattr(error, "help_message", None)
    message = str(error)
    if help_message and help_message not in message:
        message = f"{message} ({help_message})"
    return {"error": {"code": code or getattr(error, "code", None) or type(error).__name__, "message": message}}


class AppState:
    """Everything a renderer holds, as the SDK's RendererState sees it.

    RendererState validates each message as it arrives (so a top-down stream
    whose children arrive later is fine) and `check_topology` enforces the
    finished tree. One cre8-specific gap is closed on top: a JSON catalog does
    not reject unknown properties, so `unknown_property_errors` runs first.
    """

    def __init__(self) -> None:
        self.renderer = RendererState([load_catalog().api])
        self.history: dict[str, list[Message]] = {}

    def try_apply(self, messages: list[Message], *, check: bool = True) -> list[dict[str, Any]]:
        """Apply atomically; on any error nothing is applied and the errors are returned."""
        errors = unknown_property_errors(messages)
        if errors:
            return errors
        touched: set[str] = set()
        try:
            with self.renderer.transaction() as tx:
                for message in messages:
                    touched.update(tx.apply(message))
                if check:
                    tx.check_topology(touched)
        except A2uiError as e:
            return [error_detail(e)]
        for message in messages:
            surface_id = _surface_of(message)
            if surface_id:
                if "deleteSurface" in message:
                    self.history.pop(surface_id, None)
                else:
                    self.history.setdefault(surface_id, []).append(message)
        return []

    def has_surface(self, surface_id: str) -> bool:
        return surface_id in self.renderer.surface_ids

    def data_model(self, surface_id: str) -> dict[str, Any]:
        surface = self.renderer.get_surface(surface_id)
        if surface is None:
            return {}
        return surface.data_model.get("/") or {}

    def snapshot(self, surface_id: str) -> list[Message]:
        """The surface as one createSurface message: what it looks like now."""
        surface = self.renderer.get_surface(surface_id)
        if surface is None:
            return []
        # component_tree is the wire form (id, component, @metadata included).
        components = [_plain(model.component_tree) for model in surface.components_model.components_map.values()]
        body: dict[str, Any] = {"surfaceId": surface_id, "catalogId": catalog_id(), "components": components}
        data = self.data_model(surface_id)
        if data:
            body["dataModel"] = data
        return [{"version": "1.0", "createSurface": body}]


def _plain(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump(by_alias=True, exclude_none=True)
    if isinstance(value, dict):
        return {k: _plain(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_plain(v) for v in value]
    return value


def _surface_of(message: Message) -> str | None:
    for key in ("createSurface", "updateComponents", "updateDataModel", "deleteSurface"):
        body = message.get(key)
        if isinstance(body, dict):
            return body.get("surfaceId")
    return None


# a2ui-agent-sdk 0.11.0 builders and macro expansion emit the pre-final v1.0
# envelope keys (bare `catalogId`, `metadata`, ...). Final v1.0, which the pinned
# a2ui-core and the official schema enforce, spells them with an `@`.
_ENVELOPE_KEYS = ("catalogId", "metadata", "accessibility", "checks")


def normalize_components(components: list[dict[str, Any]], surface_catalog_id: str | None) -> list[dict[str, Any]]:
    allowed = load_catalog().allowed
    out = []
    for comp in components:
        comp = dict(comp)
        declared = allowed.get(comp.get("component"), frozenset())
        for key in _ENVELOPE_KEYS:
            if key in comp and key not in declared:
                value = comp.pop(key)
                if key == "catalogId" and value in (surface_catalog_id, catalog_id()):
                    continue  # redundant on a single-catalog surface
                comp[f"@{key}"] = value
        out.append(comp)
    return out


def normalize_message(message: Message) -> Message:
    for key in ("createSurface", "updateComponents"):
        body = message.get(key)
        if isinstance(body, dict) and isinstance(body.get("components"), list):
            surface_catalog = body.get("catalogId") if key == "createSurface" else catalog_id()
            return {**message, key: {**body, "components": normalize_components(body["components"], surface_catalog)}}
    return message


def to_dicts(models: Sequence[Any]) -> list[Message]:
    return [
        normalize_message(m.model_dump(by_alias=True, exclude_none=True) if hasattr(m, "model_dump") else m)
        for m in models
    ]


@lru_cache(maxsize=1)
def component_menu() -> str:
    """One line per component, for the low-effort component-selection step."""
    lines = []
    for name, schema in load_catalog().document["components"].items():
        if name == "Text":
            continue
        lines.append(f"- {name}: {schema.get('description', '')[:140]}")
    return "\n".join(lines)
