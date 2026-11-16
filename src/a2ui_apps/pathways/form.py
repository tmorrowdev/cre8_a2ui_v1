"""Form pathway: the model names the fields; Python builds and validates the form."""

from __future__ import annotations

import re
from typing import Any, ClassVar, Literal

from pydantic import BaseModel, Field

from a2ui_apps.llm import LLM
from a2ui_apps.pathways.base import Component, Message, Tree, create_surface, snake_id, update_components, update_data

FieldKind = Literal["text", "email", "number", "tel", "url", "date", "password", "select"]
MAX_FIELDS = 12
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class FormField(BaseModel):
    name: str = Field(description="snake_case key for the value, e.g. full_name")
    label: str
    kind: FieldKind = "text"
    required: bool = False
    placeholder: str | None = None
    options: list[str] = Field(default_factory=list, description="Choices, only for kind=select")


class FormSlots(BaseModel):
    title: str
    intro: str = Field(description="One sentence telling the user what the form is for")
    fields: list[FormField]
    submit_label: str = "Submit"
    success_message: str = "Thanks — we received your submission."


PLAN_SYSTEM = """You design data-entry forms. Given a request, return the form's title, a one-sentence
intro, its fields in the order a person fills them, the submit button label and the message shown
after a successful submit. Use the most specific field kind (email, tel, date, number, url,
password, select). Mark only genuinely necessary fields as required. Keep it to the fields the
request implies; at most 12."""


def normalize(slots: FormSlots) -> FormSlots:
    """Make the model's slots safe to assemble: unique snake names, sane select options, a cap."""
    seen: set[str] = set()
    fields: list[FormField] = []
    for f in slots.fields[:MAX_FIELDS]:
        name = snake_id(f.name or f.label, "field")
        base, n = name, 1
        while name in seen:
            n += 1
            name = f"{base}_{n}"
        seen.add(name)
        kind = f.kind
        options = [o for o in dict.fromkeys(o.strip() for o in f.options) if o]
        if kind == "select" and not options:
            kind = "text"
        fields.append(f.model_copy(update={"name": name, "kind": kind, "options": options if kind == "select" else []}))
    if not fields:
        fields = [FormField(name="message", label="Message", required=True)]
    return slots.model_copy(update={"fields": fields})


def _field_component(field: FormField, error: str | None = None) -> Component:
    common: dict[str, Any] = {
        "id": f"field_{field.name}",
        "label": field.label,
        "name": field.name,
        "required": field.required or None,
        "value": {"@path": f"/form/{field.name}"},
    }
    # Always explicit: @a2ui/web_core 0.15.0 keeps a prop's old value when an
    # update omits it (fixed upstream after 0.15.0, a2ui#3499), so clearing an
    # error by leaving the keys out would leave it showing.
    common.update(isError=bool(error), errorNote=error or "")
    if field.kind == "select":
        comp = {"component": "Cre8Select", "items": [{"label": o, "value": o} for o in field.options], **common}
    else:
        comp = {"component": "Cre8Field", "type": field.kind, "placeholder": field.placeholder, **common}
    return {k: v for k, v in comp.items() if v is not None}


class FormPathway:
    name: ClassVar[str] = "form"
    description: ClassVar[str] = "Collect information from a person: sign-ups, contact, registration, surveys, requests."
    # Phrases, not loose words: "a directory with a contact button" is not a form.
    keywords: ClassVar[tuple[str, ...]] = (
        "form", "sign up", "signup", "sign-up form", "register", "registration", "contact form",
        "contact us", "survey", "questionnaire", "intake", "application form", "rsvp",
        "feedback form", "booking form",
    )

    def plan(self, prompt: str, llm: LLM) -> FormSlots:
        slots = llm.structured(task="form.plan", system=[PLAN_SYSTEM], prompt=prompt, schema=FormSlots, effort="low")
        return normalize(slots)

    def _base(self, slots: FormSlots, errors: dict[str, str], status: tuple[str, str] | None) -> Tree:
        """The whole form; `status` is an optional (alert status, message) shown under the intro."""
        tree = Tree()
        title = tree.heading(slots.title, type="headline-large", tag="h1", id="title")
        intro = tree.passage(slots.intro, id="intro")
        children = [title, intro]
        if status:
            kind, message = status
            text_id = tree.text(message, id="status_text")
            children.append(tree.add("Cre8Alert", id="status", status=kind, notDismissible=True, slot_default=[text_id]))
        for f in slots.fields:
            comp = _field_component(f, errors.get(f.name))
            tree._taken.add(comp["id"])
            tree.components.append(comp)
            children.append(comp["id"])
        children.append(
            tree.add(
                "Cre8Button",
                id="submit",
                text=slots.submit_label,
                variant="primary",
                on_click={
                    "event": {
                        "name": "submit",
                        "context": {f.name: {"@path": f"/form/{f.name}"} for f in slots.fields},
                    }
                },
            )
        )
        body = tree.stack(children, gap="16", id="form_body")
        tree.components.insert(0, {"id": "root", "component": "Cre8LayoutSection", "children": [body]})
        return tree

    def assemble(self, slots: FormSlots, surface_id: str, context: dict[str, Any] | None = None) -> list[Message]:
        tree = self._base(slots, {}, None)
        data = {"form": {f.name: "" for f in slots.fields}}
        return [create_surface(surface_id, tree.components, data)]

    def errors_for(self, slots: FormSlots, values: dict[str, Any]) -> dict[str, str]:
        errors: dict[str, str] = {}
        for f in slots.fields:
            value = str(values.get(f.name) or "").strip()
            if f.required and not value:
                errors[f.name] = f"{f.label} is required."
            elif value and f.kind == "email" and not EMAIL.match(value):
                errors[f.name] = "Enter a valid email address."
            elif value and f.kind == "number":
                try:
                    float(value)
                except ValueError:
                    errors[f.name] = "Enter a number."
        return errors

    def on_action(self, slots: FormSlots, action: dict[str, Any], data: dict[str, Any], surface_id: str) -> list[Message]:
        if action.get("name") != "submit":
            return []
        values = {**(data.get("form") or {}), **(action.get("context") or {})}
        errors = self.errors_for(slots, values)
        if errors:
            status = ("error", f"Fix {len(errors)} field{'s' if len(errors) > 1 else ''} to continue.")
        else:
            status = ("success", slots.success_message)
        tree = self._base(slots, errors, status)
        messages = [update_components(surface_id, tree.components)]
        if not errors:
            messages.append(update_data(surface_id, "/submitted", values))
        return messages
