"""Freeform pathway: the model writes the UI itself, in an a2ui-agent-sdk inference format.

The least deterministic route, so it is the fallback, not the default. The SDK
does the heavy lifting: it generates the prompt from the (pruned) catalog,
parses the model's output as it streams (Express by default), and validates
every message against a RendererState. This module adds three things:

1. Component selection: a cheap structured call picks the components the app
   needs, and the catalog is pruned to them, so the prompt stays small.
2. Progressive delivery: each message is yielded the moment it validates.
3. Repair: if a stream fails, the half-built surface is deleted and the model
   gets the SDK's error and tries again, up to MAX_ATTEMPTS.
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any, ClassVar

from a2ui.core.exceptions import A2uiError
from a2ui.parser.errors import A2uiCompilationError
from a2ui.parser.response_part import A2uiPart, ErrorPart, RawA2uiPart, TextPart
from pydantic import BaseModel, Field

from a2ui_apps.examples import components_of, pick_examples
from a2ui_apps.llm import LLM
from a2ui_apps.macros import expand
from a2ui_apps.pathways.base import Message, PathwayFailed
from a2ui.parser.messages import to_message_models

from a2ui_apps.sdk import (
    EDIT_MESSAGES,
    catalog_id,
    AppState,
    DEFAULT_FORMAT,
    component_menu,
    error_detail,
    make_processor,
    to_dicts,
)
from a2ui_apps.validate import format_errors, load_catalog

MAX_ATTEMPTS = 3
# Always available, whatever the selection step picks: layout plus basic content.
BASELINE_COMPONENTS = ("HtmlDiv", "HtmlSection", "Cre8LayoutSection", "Cre8Heading", "Cre8TextPassage", "Cre8Button")

def _surface_rule(fmt: str, surface_id: str, *, edit: bool) -> str:
    """How the model targets the surface: Express-like formats default it, Direct JSON spells it out."""
    if fmt == "direct_json":
        verb = "Update the existing surface with" if edit else "Create exactly one surface with"
        return (
            f'- {verb} surfaceId "{surface_id}" and catalogId "{catalog_id()}". '
            'Every message is a JSON object with "version": "1.0".'
        )
    if edit:
        return f'- Start the block with `surface("{surface_id}", update=true)` so the host applies your changes to the existing surface.'
    return "- The host targets the surface for you: do not create, name or delete surfaces."


def app_guide(fmt: str, surface_id: str) -> str:
    return "\n".join([
        "You build one app surface for the user's request.",
        "",
        "- Write the UI top-down so it renders progressively: the root component first, then each component in the order it appears on screen, then any data model values.",
        _surface_rule(fmt, surface_id, edit=False),
        "- Before the UI, write one short sentence saying what you built. Write nothing after it.",
        "- Prefer cre8 components for all content; use the Html* containers only for grouping and layout, spacing with the token props.",
    ])


def edit_guide(fmt: str, surface_id: str, *, theme_applied: bool = False) -> str:
    theme_note = (
        ["- The host has already applied the colors, fonts, corner radius and light/dark mode this request asks for."
         " Change the UI only for what remains; if nothing else is asked, write the sentence and no UI block."]
        if theme_applied else []
    )
    return "\n".join([
        "You are editing an app the user already sees. Its current UI is in the user message.",
        "",
        *theme_note,
        _surface_rule(fmt, surface_id, edit=True),
        "- Reuse existing components by their ids; redefine only components that change, and add new ones as needed. Redefine the root only if its children change.",
        "- Change only what the request asks for, top-down.",
        "- Before the UI, write one short sentence saying what you changed. Write nothing after it.",
    ])


class ComponentSelection(BaseModel):
    components: list[str] = Field(description="Catalog component names this app needs (8-25 is typical)")


class FreeformSlots(BaseModel):
    prompt: str
    messages: list[dict[str, Any]]
    components: list[str]
    attempts: int = 1


def with_context(text: str, context: dict[str, Any] | None) -> str:
    """Append what the renderer reported (via renderer-function RPC) about the viewer."""
    if not context:
        return text
    from a2ui_apps.engine import describe_context

    return f"{text}\n\nViewer: {describe_context(context)}. Lay the app out to suit it."


def select_components(prompt: str, llm: LLM) -> list[str]:
    known = set(load_catalog().document["components"])
    choice = llm.structured(
        task="freeform.select",
        system=[
            "Pick the UI components an app for this request needs, from this catalog. "
            "Include anything needed for layout, content and interaction; omit the rest.\n" + component_menu()
        ],
        prompt=prompt,
        schema=ComponentSelection,
        effort="low",
    )
    return sorted({c for c in choice.components if c in known} | set(BASELINE_COMPONENTS))


class FreeformPathway:
    name: ClassVar[str] = "freeform"
    description: ClassVar[str] = "Anything the structured pathways do not cover; the model composes components directly."
    keywords: ClassVar[tuple[str, ...]] = ()

    def __init__(self, fmt: str = DEFAULT_FORMAT, examples: Sequence[Sequence[Message]] | None = None) -> None:
        self.fmt = fmt
        self.examples = examples

    def run(
        self, prompt: str, llm: LLM, *, surface_id: str, state: AppState, context: dict[str, Any] | None = None
    ) -> Iterator[dict[str, Any]]:
        """Build a new surface. Yields {"text"}, {"a2ui"}, {"step"}; returns FreeformSlots."""
        components = select_components(prompt, llm)
        examples, components = self._with_examples(components)
        yield {"step": {"name": "select", "deterministic": False, "detail": f"{len(components)} components, {len(examples)} example(s)"}}
        processor = make_processor(surface_id=surface_id, fmt=self.fmt, components=components, examples=examples)
        messages = yield from self._attempts(
            processor,
            system=[processor.prompt_snippet, app_guide(self.fmt, surface_id)],
            user=with_context(prompt, context),
            llm=llm,
            state=state,
            surface_id=surface_id,
            require_create=True,
            restore=[{"version": "1.0", "deleteSurface": {"surfaceId": surface_id}}],
        )
        return FreeformSlots(prompt=prompt, messages=messages[0], components=components, attempts=messages[1])

    def edit(
        self,
        prompt: str,
        llm: LLM,
        *,
        surface_id: str,
        state: AppState,
        context: dict[str, Any] | None = None,
        theme_applied: bool = False,
    ) -> Iterator[dict[str, Any]]:
        """Change a live surface (canvas mode). Same contract as `run`."""
        snapshot = state.snapshot(surface_id)
        in_use = {c["component"] for c in snapshot[0]["createSurface"]["components"]}
        examples, components = self._with_examples(sorted(set(select_components(prompt, llm)) | in_use))
        yield {"step": {"name": "select", "deterministic": False, "detail": f"{len(components)} components ({len(in_use)} in use), {len(examples)} example(s)"}}
        processor = make_processor(
            surface_id=surface_id, fmt=self.fmt, components=components, allowed_messages=EDIT_MESSAGES, examples=examples
        )
        # wrap() takes raw parts and silently drops plain strings; each format adds its own tags.
        current = processor.parser.wrap([RawA2uiPart(a2ui_raw=processor.parser.decompile(to_message_models(snapshot)))])
        messages = yield from self._attempts(
            processor,
            system=[processor.prompt_snippet, edit_guide(self.fmt, surface_id, theme_applied=theme_applied)],
            user=with_context(f"Current UI:\n{current}\n\nChange request: {prompt}", context),
            llm=llm,
            state=state,
            surface_id=surface_id,
            require_create=False,
            preload=snapshot,
            allow_empty=theme_applied,
            # Edits already streamed to the browser are undone by redrawing the snapshot.
            restore=[{"version": "1.0", "deleteSurface": {"surfaceId": surface_id}}, *snapshot],
        )
        return FreeformSlots(prompt=prompt, messages=messages[0], components=components, attempts=messages[1])

    def _with_examples(self, components: list[str]) -> tuple[list[Any], list[str]]:
        """Few-shot examples for this selection, and the selection widened to cover them.

        An example may only use components the pruned prompt still describes, so
        its components join the selection. Explicit `examples` win if given.
        """
        chosen = [list(e) for e in self.examples] if self.examples is not None else pick_examples(set(components))
        widened = set(components)
        for example in chosen:
            widened |= components_of(example)
        return [to_message_models(e) for e in chosen], sorted(widened)

    def _attempts(
        self,
        processor: Any,
        *,
        system: list[str],
        user: str,
        llm: LLM,
        state: AppState,
        surface_id: str,
        require_create: bool,
        restore: list[Message],
        preload: list[Message] | None = None,
        allow_empty: bool = False,
    ) -> Iterator[dict[str, Any]]:
        """Stream, validate, and repair. Returns (messages, attempts) once a stream is accepted."""
        conversation: list[dict[str, Any]] = [{"role": "user", "content": user}]
        errors: list[dict[str, Any]] = []
        for attempt in range(1, MAX_ATTEMPTS + 1):
            emitted: list[Message] = []
            reply = ""
            errors = []
            parser_state = processor.create_state()
            for message in to_message_models(preload or []):
                parser_state.apply(message)
            stream = processor.open_stream(state=parser_state)
            try:
                for chunk in llm.stream_text(task="freeform.generate", system=system, messages=conversation, effort="high"):
                    reply += chunk
                    yield from self._parts(stream.feed(chunk), emitted, errors)
                yield from self._parts(stream.close(), emitted, errors)
                targets = {sid for m in emitted for body in m.values() if isinstance(body, dict) and (sid := body.get("surfaceId"))}
                if require_create and not any("createSurface" in m for m in emitted):
                    errors.append({"error": {"code": "NO_UI", "message": "The response contained no UI block."}})
                elif targets - {surface_id}:
                    errors.append({"error": {"code": "WRONG_SURFACE", "message": f'Use surfaceId "{surface_id}" only; got {sorted(targets - {surface_id})}.'}})
                elif not require_create and not emitted and not allow_empty:
                    errors.append({"error": {"code": "NO_CHANGE", "message": "The response changed nothing."}})
            except (A2uiError, A2uiCompilationError) as e:
                errors.append(error_detail(e))
            if not errors:
                errors = state.try_apply(emitted)
            if not errors:
                return emitted, attempt

            if emitted:
                # Remove anything the browser was sent on a surface the model should not have created.
                for stray in sorted({m["createSurface"]["surfaceId"] for m in emitted if "createSurface" in m} - {surface_id}):
                    yield {"a2ui": {"version": "1.0", "deleteSurface": {"surfaceId": stray}}}
                for message in restore:
                    yield {"a2ui": message}
            yield {"step": {"name": "repair", "deterministic": False, "detail": f"attempt {attempt}: {format_errors(errors)[:160]}"}}
            conversation += [
                {"role": "assistant", "content": reply or "(no output)"},
                {
                    "role": "user",
                    "content": "That output was rejected. Fix every problem and write the complete UI block again.\n"
                    + format_errors(errors),
                },
            ]
        raise PathwayFailed(f"freeform generation still invalid after {MAX_ATTEMPTS} attempts", errors)

    @staticmethod
    def _parts(parts: list[Any], emitted: list[Message], errors: list[dict[str, Any]]) -> Iterator[dict[str, Any]]:
        for part in parts:
            if isinstance(part, TextPart):
                if part.text.strip():
                    yield {"text": part.text}
            elif isinstance(part, A2uiPart):
                # Lower macros to cre8 primitives before anything leaves the agent.
                for message in to_dicts(expand(part.a2ui)):
                    emitted.append(message)
                    yield {"a2ui": message}
            elif isinstance(part, ErrorPart):
                errors.append(error_detail(part.error))

    # Deterministic-pathway interface, kept so the engine can treat pathways uniformly.
    def on_action(self, slots: BaseModel, action: dict[str, Any], data: dict[str, Any], surface_id: str) -> list[Message]:
        return []
