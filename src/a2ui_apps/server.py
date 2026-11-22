"""HTTP transport: request/response A2UI over JSONL.

POST /api/generate  {prompt}            -> application/jsonl: A2UI messages, then a trace line
POST /api/action    {action envelope}   -> application/jsonl: A2UI messages answering it
POST /api/rpc       {renderer message}  -> application/jsonl: agentFunctionResponse replies
GET  /api/catalog                        -> the cre8 v1.0 catalog the renderer registers

This is the spec's request-response transport pattern: the renderer posts an
action, the agent answers with the messages it causes. `sendDataModel` surfaces
also post their data model, which the action handler receives.

Run: uv run uvicorn a2ui_apps.server:app --reload
Set A2UI_APPS_FAKE_LLM=1 to serve canned plans (no API key, deterministic).
Model stack (planner, optional fine-tuned composer): see a2ui_apps.composer.llm_from_env.
"""

from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator
from typing import Any, Iterable

import anthropic
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

from a2ui_apps.engine import Engine
from a2ui_apps.llm import LLM, LLMIncomplete, LLMRefusal
from a2ui_apps.pathways.base import PathwayFailed
from a2ui_apps.rpc import CONTEXT_FUNCTIONS, RpcHub
from a2ui_apps.sdk import FORMATS
from a2ui_apps.validate import load_catalog


class GenerateRequest(BaseModel):
    prompt: str
    format: str | None = None
    surfaceId: str | None = None  # set to edit that live surface instead of building a new one
    rendererFunctions: bool = False  # the client implements getViewport/getPreferences and posts to /api/rpc


class ActionRequest(BaseModel):
    message: dict[str, Any]
    dataModel: dict[str, Any] | None = None


def _jsonl(items: Iterable[dict[str, Any]]) -> StreamingResponse:
    return StreamingResponse((json.dumps(item) + "\n" for item in items), media_type="application/jsonl")


def create_app(llm: LLM | None = None) -> FastAPI:
    if llm is None:
        from a2ui_apps.composer import llm_from_env

        llm = llm_from_env()
    engine = Engine(llm)
    hub = RpcHub()
    app = FastAPI(title="a2ui-apps")

    @app.get("/api/catalog")
    def catalog() -> JSONResponse:
        return JSONResponse(load_catalog().document)

    @app.post("/api/generate")
    async def generate(req: GenerateRequest) -> StreamingResponse:
        if req.format and req.format not in FORMATS:
            raise HTTPException(400, {"message": f"unknown format {req.format!r}; choose from {sorted(FORMATS)}"})

        async def events() -> AsyncIterator[str]:
            # Headers go out before generation finishes, so failures become an
            # {"error"} line rather than an HTTP status.
            context: dict[str, Any] = {}
            if req.rendererFunctions:
                # Agent -> renderer RPC: ask, then wait for answers posted to /api/rpc.
                asks = []
                for name in CONTEXT_FUNCTIONS:
                    message, future = hub.ask(name)
                    asks.append((name, future))
                    yield json.dumps({"a2ui": message}) + "\n"
                context = await hub.gather(asks)
            stream = engine.stream(req.prompt, fmt=req.format, surface_id=req.surfaceId, context=context)
            done = object()
            while True:
                try:
                    event = await asyncio.to_thread(next, stream, done)  # the engine blocks on model calls
                except PathwayFailed as e:
                    event = {"error": {"message": str(e), "errors": e.errors}}
                except KeyError as e:
                    event = {"error": {"message": str(e)}}
                except LLMRefusal as e:
                    event = {"error": {"message": f"The model declined: {e}"}}
                except LLMIncomplete as e:
                    event = {"error": {"message": str(e)}}
                except anthropic.RateLimitError:
                    event = {"error": {"message": "Model rate limit reached; try again shortly."}}
                except anthropic.APIStatusError as e:
                    event = {"error": {"message": f"Model API error {e.status_code}"}}
                except anthropic.APIConnectionError:
                    event = {"error": {"message": "Could not reach the model API."}}
                if event is done:
                    return
                yield json.dumps(event) + "\n"
                if "error" in event:
                    return

        return StreamingResponse(events(), media_type="application/jsonl")

    @app.post("/api/rpc")
    async def rpc(message: dict[str, Any]) -> StreamingResponse:
        """Renderer -> agent messages: callAgentFunction, rendererFunctionResponse, error."""
        if message.get("version") != "1.0":
            raise HTTPException(400, {"message": "expected an A2UI v1.0 renderer-to-agent message"})
        try:
            replies = await hub.handle(message)
        except Exception as e:  # malformed message: the SDK raises on shapes it cannot read
            raise HTTPException(400, {"message": str(e)})
        return _jsonl(replies)

    @app.post("/api/action")
    def action(req: ActionRequest) -> StreamingResponse:
        if "action" not in req.message:
            raise HTTPException(400, {"message": "expected an action envelope"})
        try:
            messages = engine.handle_action(req.message, req.dataModel)
        except KeyError as e:
            raise HTTPException(404, {"message": str(e)})
        except PathwayFailed as e:
            raise HTTPException(422, {"message": str(e), "errors": e.errors})
        return _jsonl(messages)

    return app


app = create_app()
