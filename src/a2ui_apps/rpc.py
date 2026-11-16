"""Function RPC in both directions, on a2ui-agent-sdk.

- Agent -> renderer: `RendererFunctionCalls.call` builds a `callRendererFunction`
  message and a future; the renderer runs its implementation and posts back a
  `rendererFunctionResponse`, which settles the future.
- Renderer -> agent: `RendererToAgentMessageProcessor` answers `callAgentFunction`
  by running the catalog's agent functions (see agent_functions.py).

Over HTTP (request/response), agent-initiated calls ride the generation stream
and every renderer-to-agent message is POSTed to /api/rpc.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from a2ui.rpc.processor import RendererToAgentMessageProcessor
from a2ui.rpc.renderer_function_calls import RendererFunctionCalls

from a2ui_apps.validate import load_catalog

log = logging.getLogger(__name__)

# What the agent asks the renderer before it builds an app.
CONTEXT_FUNCTIONS = ("getViewport", "getPreferences")


def _dump(model: Any) -> dict[str, Any]:
    return model.model_dump(by_alias=True, exclude_unset=True) if hasattr(model, "model_dump") else dict(model)


class RpcHub:
    def __init__(self, timeout: float = 4.0) -> None:
        catalogs = [load_catalog().api]
        self.timeout = timeout
        self.calls = RendererFunctionCalls(default_timeout=timeout, catalogs=catalogs)
        self.errors: list[dict[str, Any]] = []
        self.processor = RendererToAgentMessageProcessor(
            catalogs,
            agent_function_timeout=timeout,
            on_renderer_function_response=self.calls.resolve,
            on_error=self._on_error,
        )

    def _on_error(self, message: Any) -> None:
        self.errors.append(_dump(message))
        log.warning("renderer reported an error: %s", self.errors[-1])

    async def handle(self, message: dict[str, Any]) -> list[dict[str, Any]]:
        """One renderer-to-agent message in, the agent's replies out."""
        result = await self.processor.process_message(message)
        return [_dump(reply) for reply in result.replies]

    def ask(self, name: str, args: dict[str, Any] | None = None) -> tuple[dict[str, Any], asyncio.Future]:
        message, future = self.calls.call(catalog_id=load_catalog().catalog_id, name=name, args=args or {})
        return _dump(message), future

    async def gather(self, asks: list[tuple[str, asyncio.Future]]) -> dict[str, Any]:
        """Await renderer answers; a missing or failed answer is simply left out."""
        context: dict[str, Any] = {}
        for name, future in asks:
            try:
                context[name] = await asyncio.wait_for(future, self.timeout)
            except Exception as e:  # timeout, renderer error, cancelled: generate without it
                log.info("renderer function %s gave no answer: %s", name, e)
        return context
