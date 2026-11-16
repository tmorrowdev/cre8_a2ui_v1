"""What a pathway is, and the deterministic helpers every assembler shares."""

from __future__ import annotations

import re
from typing import Any, ClassVar, Protocol

from pydantic import BaseModel

from a2ui_apps.llm import LLM
from a2ui_apps.validate import load_catalog

Message = dict[str, Any]
Component = dict[str, Any]


class PathwayFailed(RuntimeError):
    def __init__(self, message: str, errors: list[dict[str, Any]] | None = None):
        super().__init__(message)
        self.errors = errors or []


class Pathway(Protocol):
    """A route from a prompt to a validated surface.

    `plan` is the only step that may call the model. `assemble` and `on_action`
    are pure functions of their inputs, which is what makes a pathway
    semi-deterministic: same slots in, same messages out.
    """

    name: ClassVar[str]
    description: ClassVar[str]
    keywords: ClassVar[tuple[str, ...]]

    def plan(self, prompt: str, llm: LLM) -> BaseModel: ...

    def assemble(self, slots: BaseModel, surface_id: str, context: dict[str, Any] | None = None) -> list[Message]: ...

    def on_action(
        self, slots: BaseModel, action: dict[str, Any], data: dict[str, Any], surface_id: str
    ) -> list[Message]: ...


def snake_id(text: str, fallback: str = "item") -> str:
    """A UAX #31-safe snake_case identifier derived from free text."""
    ident = re.sub(r"[^0-9a-zA-Z]+", "_", text).strip("_").lower()
    if not ident:
        ident = fallback
    if ident[0].isdigit():
        ident = f"{fallback}_{ident}"
    return ident


class Tree:
    """Collects a flat v1.0 component list with unique, readable ids."""

    def __init__(self) -> None:
        self.components: list[Component] = []
        self._taken: set[str] = set()

    def _claim(self, base: str) -> str:
        candidate, n = base, 1
        while candidate in self._taken:
            n += 1
            candidate = f"{base}_{n}"
        self._taken.add(candidate)
        return candidate

    def add(self, component: str, *, id: str | None = None, **props: Any) -> str:
        cid = self._claim(id or snake_id(component.removeprefix("Cre8"), "node"))
        self.components.append({"id": cid, "component": component, **{k: v for k, v in props.items() if v is not None}})
        return cid

    def text(self, value: str, *, id: str | None = None) -> str:
        return self.add("Text", id=id or "text", text=value)

    def heading(self, value: str, *, type: str, tag: str | None = None, id: str | None = None) -> str:
        return self.add("Cre8Heading", id=id, type=type, tagVariant=tag, children=[self.text(value)])

    def passage(self, value: str, *, id: str | None = None) -> str:
        return self.add("Cre8TextPassage", id=id, children=[self.text(value)])

    def stack(self, children: list[str], *, gap: str = "16", id: str | None = None, element: str = "HtmlDiv") -> str:
        """A structural flex column; spacing is a cre8 token, so it travels with the surface."""
        return self.add(element, id=id or "stack", display="flex", direction="column", gap=gap, children=children)


def create_surface(surface_id: str, components: list[Component], data: dict[str, Any] | None = None) -> Message:
    body: dict[str, Any] = {
        "surfaceId": surface_id,
        "catalogId": load_catalog().catalog_id,
        "sendDataModel": True,
        "components": components,
    }
    if data:
        body["dataModel"] = data
    return {"version": "1.0", "createSurface": body}


def update_components(surface_id: str, components: list[Component]) -> Message:
    return {"version": "1.0", "updateComponents": {"surfaceId": surface_id, "components": components}}


def update_data(surface_id: str, path: str, value: Any) -> Message:
    return {"version": "1.0", "updateDataModel": {"surfaceId": surface_id, "path": path, "value": value}}
