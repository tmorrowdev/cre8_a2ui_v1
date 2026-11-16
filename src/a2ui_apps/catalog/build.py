"""Build an A2UI v1.0 catalog from the catalog cre8-wc ships.

cre8-wc publishes `a2ui/catalog.json` in its own nested format, keyed by tag
(`cre8-button`). v1.0 requires UAX #31 identifiers for component types and
property names, so the v1.0 vocabulary is a reversible mapping, the same one
cre8-mcp's `a2ui_v1` tool uses:

    cre8-button          -> Cre8Button
    prop aria-label      -> ariaLabel       (only where the name is not UAX #31)
    slot footer          -> slot_footer     (slots and props share names, e.g. fieldNote)
    children             -> children        (ChildList)
    event tab-change     -> on_tab_change   (common_types Action)
    text node            -> Text { text }

Run `python -m a2ui_apps.catalog.build <path to cre8-wc a2ui/catalog.json>` to
regenerate `cre8_wc.v1.json` after bumping cre8-wc. `x-cre8-prop`, `x-cre8-slot` and
`x-cre8-event` annotations carry the original cre8 names back to the renderer.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from a2ui_apps.catalog.html import html_components, style_defs

PROTOCOL_VERSION = "1.0"
TEXT_COMPONENT = "Text"
SLOT_PREFIX = "slot_"
EVENT_PREFIX = "on_"
COMMON = "common_types.json#/$defs/"
RESERVED = {"id", "component"}
# Native DOM events exposed as on_* actions. cre8-wc lists 46; an app agent needs
# these, and the rest (hover, drag, touch, clipboard) multiply prompt size by ~10x.
AGENT_EVENTS = {"click", "change", "input", "submit", "keydown", "focus", "blur"}

CATALOG_PATH = Path(__file__).with_name("cre8_wc.v1.json")

INSTRUCTIONS = "\n".join(
    [
        "Every component is a cre8 web component; `x-cre8-tag` on each definition names the element it renders.",
        "Text content is a separate `Text` component referenced from `children` or a `slot_*` property, never a string in a ChildList.",
        "Content goes through EITHER `children` OR `slot_*` properties; the definition says which. Button labels are the `text` property.",
        "Any non-static property can be bound to the data model, and lists of children can be generated from a data model list with a template.",
        "Events: `on_<event>` properties take an Action whose event.name is reported back to the agent.",
        'Every component accepts token spacing: padding, paddingX, paddingY, margin, marginX, marginY ("0"-"96"; 16 = 1rem).',
        "Html* components are structural HTML containers (div, section, article, aside, header, footer, nav) for grouping and layout only. They take display, direction, gap, align, justify, wrap, columns, background, radius, border, width, maxWidth and textAlign, all as cre8 token enums. All content (text, headings, lists, links, images) is cre8 components.",
    ]
)


def _renderer_function(name: str, description: str, return_type: str) -> dict[str, Any]:
    """A function the browser implements and only the agent calls (callRendererFunction)."""
    return {
        "type": "object",
        "description": description,
        "returnType": return_type,
        "allowedCallers": "agentOnly",
        "properties": {"@call": {"const": name}},
        "required": ["@call"],
    }


# Implemented by the renderer (web/src/main.ts); the agent asks before it generates.
RENDERER_FUNCTIONS: dict[str, Any] = {
    "getViewport": _renderer_function("getViewport", "The renderer's viewport size in CSS pixels: {width, height}.", "object"),
    "getPreferences": _renderer_function(
        "getPreferences", "The viewer's display preferences: {colorScheme, reducedMotion, locale}.", "object"
    ),
}


def is_uax31(name: str) -> bool:
    """Python's identifier rule is UAX #31: XID_Start or "_", then XID_Continue."""
    return name.isidentifier()


def pascal(tag: str) -> str:
    return "".join(part[:1].upper() + part[1:] for part in re.split(r"[^A-Za-z0-9]+", tag) if part)


def camel(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]+([A-Za-z0-9])", lambda m: m.group(1).upper(), name)


def event_prop(event: str) -> str:
    return EVENT_PREFIX + re.sub(r"[^A-Za-z0-9_]+", "_", event)


@dataclass
class ComponentMapping:
    tag: str
    type: str
    definition: dict[str, Any]
    props: dict[str, str] = field(default_factory=dict)  # cre8 prop -> v1 property
    slots: dict[str, str] = field(default_factory=dict)  # cre8 slot -> v1 property
    events: dict[str, str] = field(default_factory=dict)  # custom event -> v1 property
    accepts_children: bool = False


@dataclass
class Mapping:
    catalog_id: str
    library_version: str
    native_events: dict[str, str]
    components: dict[str, ComponentMapping]  # by v1 type


def build_mapping(source: dict[str, Any]) -> Mapping:
    meta = source.get("x-a2ui", {})
    version = meta.get("libraryVersion", "unversioned")
    catalog_id = f"https://cre8.dev/a2ui/v1_0/catalogs/{meta.get('catalogId', 'cre8-wc')}/{version}"
    native = {event: event_prop(event) for event in source.get("x-native-events", []) if event in AGENT_EVENTS}

    components: dict[str, ComponentMapping] = {}
    for tag, definition in source["$defs"]["components"].items():
        type_name = pascal(tag)
        if not is_uax31(type_name) or type_name in (TEXT_COMPONENT, "Surface") or type_name in components:
            raise ValueError(f"{tag}: v1 type {type_name!r} is invalid or already taken")
        used: dict[str, str] = {v1: f"event {ev}" for ev, v1 in native.items()}
        used.update({key: "(reserved)" for key in RESERVED})

        def claim(v1: str, owner: str) -> str:
            if not is_uax31(v1):
                raise ValueError(f"{tag}: {owner} maps to {v1!r}, which is not UAX #31")
            if v1 in used:
                raise ValueError(f"{tag}: {owner} and {used[v1]} both map to {v1!r}")
            used[v1] = owner
            return v1

        props = definition.get("properties", {})
        m = ComponentMapping(tag=tag, type=type_name, definition=definition)
        m.accepts_children = "children" in props
        if m.accepts_children:
            claim("children", "children")
        for prop in (props.get("props") or {}).get("properties", {}):
            m.props[prop] = claim(prop if is_uax31(prop) else camel(prop), f"prop {prop}")
        for slot in (props.get("slots") or {}).get("properties", {}):
            m.slots[slot] = claim(SLOT_PREFIX + re.sub(r"[^A-Za-z0-9_]+", "_", slot), f"slot {slot}")
        for event in definition.get("x-events", {}):
            if event not in native:
                m.events[event] = claim(event_prop(event), f"event {event}")
        components[type_name] = m

    return Mapping(catalog_id=catalog_id, library_version=version, native_events=native, components=components)


def brief(text: str | None, limit: int = 160) -> str | None:
    """The first sentence of a cre8 doc string: the catalog feeds model prompts,
    and the full docs (bullet lists, import examples, links) are written for people."""
    if not text:
        return None
    first = next((line.strip() for line in text.splitlines() if line.strip() and not line.strip().startswith(("-", "*", "#", "["))), "")
    first = re.split(r"(?<=[.!?])\s", first, maxsplit=1)[0].strip()
    if len(first) > limit:
        first = first[: limit - 1].rsplit(" ", 1)[0] + "…"
    return first or None


def _dynamic(prop_schema: dict[str, Any]) -> dict[str, Any]:
    """A literal matching the cre8 prop schema, a data binding, or a function call."""
    literal = {k: v for k, v in prop_schema.items() if k not in ("description", "default")}
    out: dict[str, Any] = {"anyOf": [literal, {"$ref": f"{COMMON}DataBinding"}, {"$ref": f"{COMMON}FunctionCall"}]}
    if description := brief(prop_schema.get("description")):
        out["description"] = description
    return out


def _component_schema(m: ComponentMapping) -> dict[str, Any]:
    properties: dict[str, Any] = {"component": {"const": m.type}}
    prop_defs = (m.definition["properties"].get("props") or {}).get("properties", {})
    for prop, v1 in m.props.items():
        properties[v1] = _dynamic(prop_defs[prop])
        if v1 != prop:
            properties[v1]["x-cre8-prop"] = prop
    if m.accepts_children:
        properties["children"] = {"$ref": f"{COMMON}ChildList", "description": "A list of child components, in order, even if there is only one."}
    slot_descriptions = m.definition.get("x-slot-descriptions", {})
    for slot, v1 in m.slots.items():
        properties[v1] = {
            "$ref": f"{COMMON}ChildList",
            # Always a list, even for one child: the model otherwise passes a bare component.
            "description": f'A list of components for the "{slot}" slot, even if there is only one.'
            + (f" {d}" if (d := brief(slot_descriptions.get(slot))) else ""),
            "x-cre8-slot": slot,
        }
    for event, v1 in m.events.items():
        properties[v1] = {"$ref": f"{COMMON}Action", "description": f'Fires on the "{event}" event.', "x-cre8-event": event}
    summary = brief(m.definition.get("description"), 200) or ""
    schema: dict[str, Any] = {
        "type": "object",
        "title": m.type,
        "description": f"<{m.tag}>" + (f" — {summary}" if summary else ""),
        "x-cre8-tag": m.tag,
        "allOf": [
            {"$ref": "#/$defs/NativeEventHandlers"},
            {"$ref": "#/$defs/SpacingProps"},
            {"type": "object", "properties": properties, "required": ["component"]},
        ],
    }
    if m.definition.get("x-category"):
        schema["x-category"] = m.definition["x-category"]
    return schema


def build_catalog(source: dict[str, Any]) -> dict[str, Any]:
    mapping = build_mapping(source)
    components: dict[str, Any] = {
        TEXT_COMPONENT: {
            "type": "object",
            "title": TEXT_COMPONENT,
            "description": "A plain text node inside a cre8 component. Wrap it in Cre8Heading or Cre8TextPassage for typography.",
            "properties": {
                "component": {"const": TEXT_COMPONENT},
                "text": {"type": "string", "description": "The literal text."},
            },
            "required": ["component", "text"],
        }
    }
    for type_name, m in mapping.components.items():
        components[type_name] = _component_schema(m)
    html = html_components()
    if clash := set(html) & set(components):
        raise ValueError(f"HTML element types collide with cre8 types: {sorted(clash)}")
    components.update(html)

    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": mapping.catalog_id,
        "protocolVersion": PROTOCOL_VERSION,
        "title": f"cre8-wc {mapping.library_version} A2UI v1.0 catalog",
        "description": f"The {len(mapping.components)} cre8-wc web components plus {len(html)} structural HTML elements, expressed as an A2UI v1.0 catalog.",
        "catalogId": mapping.catalog_id,
        "instructions": INSTRUCTIONS,
        "components": components,
        "functions": RENDERER_FUNCTIONS,
        "$defs": {
            "anyComponent": {
                "oneOf": [{"$ref": f"#/components/{name}"} for name in components],
                "discriminator": {"propertyName": "component"},
            },
            "anyFunction": {"oneOf": [{"$ref": f"#/functions/{name}"} for name in RENDERER_FUNCTIONS]},
            "NativeEventHandlers": {
                "type": "object",
                "description": "Native DOM events bindable on any cre8 component.",
                "properties": {
                    v1: {"$ref": f"{COMMON}Action", "description": f'Fires on the native "{event}" event.', "x-cre8-event": event}
                    for event, v1 in mapping.native_events.items()
                },
            },
            **style_defs(),
        },
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python -m a2ui_apps.catalog.build <cre8-wc a2ui/catalog.json>", file=sys.stderr)
        return 2
    source = json.loads(Path(argv[1]).read_text())
    catalog = build_catalog(source)
    CATALOG_PATH.write_text(json.dumps(catalog, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {CATALOG_PATH} ({len(catalog['components'])} components, {catalog['catalogId']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
