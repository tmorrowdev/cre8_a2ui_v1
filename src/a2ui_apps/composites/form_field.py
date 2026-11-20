"""FormField: a labelled input bound to the data model."""

from __future__ import annotations

from typing import Literal

from a2ui.builder.v1_0 import DataBinding
from a2ui.transformers.macros import macro

from a2ui_apps.builders.cre8 import Cre8Field


@macro
def FormField(
    label: str,
    path: str,
    kind: Literal["text", "email", "number", "tel", "url", "date", "password"] = "text",
    required: bool = False,
    placeholder: str = "",
) -> Cre8Field:
    """A labelled input whose value is two-way bound to the data model.

    Args:
        label: Visible label.
        path: Absolute data model path the value is bound to, e.g. "/form/email".
        kind: Input type.
        required: Whether the field must be filled.
        placeholder: Hint text shown when empty.
    """
    return Cre8Field(
        label=label,
        type=kind,
        required=required or None,
        placeholder=placeholder or None,
        value=DataBinding(path=path),
    )
