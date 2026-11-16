"""Validation: a2ui_core STRICT plus the one check it skips for JSON catalogs.

a2ui_core validates a component against its catalog schema. The basic catalog's
components are pydantic models that forbid extra fields, but a JSON catalog's
are not, and the official envelope's `unevaluatedProperties: false` is applied
where a catalog cannot express it (around ComponentCommon). So an unknown
property on a cre8 component would pass silently. `unknown_property_errors`
closes that gap in the same error format a2ui_core uses.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

from a2ui.core.catalog import Catalog
from a2ui.core.processing import MessageProcessor, MessageProcessorOptions
from a2ui.core.validation.payload_validator import STRICT_VALIDATION

from a2ui_apps.catalog.build import CATALOG_PATH

ENVELOPE_KEYS = {"id", "component", "@catalogId", "@metadata", "@accessibility", "@checks"}

Message = dict[str, Any]
ErrorDetail = dict[str, Any]


@dataclass(frozen=True)
class LoadedCatalog:
    document: dict[str, Any]
    api: Any
    allowed: dict[str, frozenset[str]]

    @property
    def catalog_id(self) -> str:
        return self.document["catalogId"]


@lru_cache(maxsize=1)
def load_catalog() -> LoadedCatalog:
    document = json.loads(CATALOG_PATH.read_text())
    defs = document["$defs"]
    allowed: dict[str, frozenset[str]] = {}
    for name, schema in document["components"].items():
        keys = set(schema.get("properties", {}))
        for part in schema.get("allOf", []):
            ref = part.get("$ref", "")
            # Traits (NativeEventHandlers, SpacingProps, BoxStyle) live in $defs.
            source = defs[ref.removeprefix("#/$defs/")] if ref.startswith("#/$defs/") else part
            keys |= set(source.get("properties", {}))
        allowed[name] = frozenset(keys | ENVELOPE_KEYS)
    # The agent's copy of the catalog also declares the agent functions, so
    # validation, prompts and the document served to the renderer all know them.
    from a2ui_apps.agent_functions import AGENT_FUNCTIONS

    api = Catalog.from_json(document, protocol_version="1.0").copy_with(agent_functions=AGENT_FUNCTIONS)
    return LoadedCatalog(document=api.to_json(), api=api, allowed=allowed)


def _components_of(message: Message) -> tuple[str, list[Any]] | None:
    for key in ("createSurface", "updateComponents"):
        body = message.get(key)
        if isinstance(body, dict) and isinstance(body.get("components"), list):
            return body.get("surfaceId", ""), body["components"]
    return None


def unknown_property_errors(messages: list[Message]) -> list[ErrorDetail]:
    allowed = load_catalog().allowed
    errors: list[ErrorDetail] = []
    for message in messages:
        found = _components_of(message)
        if not found:
            continue
        surface_id, components = found
        for i, comp in enumerate(components):
            if not isinstance(comp, dict) or comp.get("component") not in allowed:
                continue  # a2ui_core reports unknown types and malformed entries
            for key in comp:
                if key not in allowed[comp["component"]]:
                    errors.append(
                        {
                            "version": "1.0",
                            "error": {
                                "code": "VALIDATION_FAILED",
                                "message": f"Unknown property '{key}' on component '{comp.get('id')}' ({comp['component']})",
                                "surfaceId": surface_id,
                                "path": f"/components/{i}/{key}",
                            },
                        }
                    )
    return errors


def new_processor() -> MessageProcessor:
    return MessageProcessor(
        [load_catalog().api],
        options=MessageProcessorOptions(validation_config=STRICT_VALIDATION),
    )


def validate_messages(messages: list[Message]) -> list[ErrorDetail]:
    """Errors (renderer error envelopes) for a self-contained message batch; [] when valid."""
    errors = unknown_property_errors(messages)
    if errors:
        return errors
    return list(new_processor().process_messages_with_errors(messages))


def format_errors(errors: list[ErrorDetail]) -> str:
    """One line per error, for feeding back into a repair prompt."""
    lines = []
    for e in errors:
        err = e.get("error", e)
        path = err.get("path")
        lines.append(f"- [{err.get('code')}] {path + ': ' if path else ''}{err.get('message')}")
    return "\n".join(lines)
