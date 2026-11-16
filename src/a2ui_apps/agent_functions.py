"""Agent functions: catalog functions the renderer calls and the agent runs.

A generated UI can bind a property to one (e.g. `text=daysUntil($/event/date)`).
The renderer has no implementation, so it sends `callAgentFunction`; the SDK's
RendererToAgentMessageProcessor validates the arguments against the schema
below, runs the handler, and answers with `agentFunctionResponse`.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any

from a2ui.core.catalog.functions import AgentFunction


def _days_until(args: dict[str, Any]) -> int:
    target = date.fromisoformat(str(args["date"])[:10])
    return (target - datetime.now(timezone.utc).date()).days


def _word_count(args: dict[str, Any]) -> int:
    return len(str(args.get("text") or "").split())


AGENT_FUNCTIONS = [
    AgentFunction(
        "daysUntil",
        handler=_days_until,
        return_type="number",
        description="Whole days from today (UTC) until a date (YYYY-MM-DD); negative if past.",
        schema={
            "type": "object",
            # Dynamic: in a UI binding the argument is itself usually a data binding.
            "properties": {"date": {"$ref": "common_types.json#/$defs/DynamicString", "description": "An ISO date, YYYY-MM-DD."}},
            "required": ["date"],
            "additionalProperties": False,
        },
    ),
    AgentFunction(
        "wordCount",
        handler=_word_count,
        return_type="number",
        description="The number of whitespace-separated words in a text.",
        schema={
            "type": "object",
            "properties": {"text": {"$ref": "common_types.json#/$defs/DynamicString"}},
            "required": ["text"],
            "additionalProperties": False,
        },
    ),
]
