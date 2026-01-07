import json
import os
import re
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from travel_agent.app import build_graph

@asynccontextmanager
async def _lifespan(_: FastAPI):
    global _graph
    _graph = build_graph()
    yield


app = FastAPI(lifespan=_lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


_graph = None


def _result_text(node_result: Any) -> str:
    if not node_result:
        return ""
    result = getattr(node_result, "result", None)
    message = getattr(result, "message", None) if result else None
    content = getattr(message, "content", None) if message else None
    if content:
        chunks = []
        for block in content:
            text = getattr(block, "text", None)
            if text:
                chunks.append(text)
        if chunks:
            return "\n".join(chunks)
    return str(result) if result is not None else ""


def _json_safe(value: Any) -> Any:
    if value is None:
        return None
    enum_value = getattr(value, "value", None)
    if enum_value is not None:
        return enum_value
    return str(value)


def _parse_json(text: str) -> Optional[Any]:
    if not text:
        return None
    fence_match = re.search(r"```json\s*([\s\S]*?)```", text, re.IGNORECASE)
    raw = fence_match.group(1) if fence_match else text
    decoder = json.JSONDecoder()
    for idx, char in enumerate(raw):
        if char in "{[":
            try:
                value, _ = decoder.raw_decode(raw[idx:])
                return value
            except json.JSONDecodeError:
                continue
    return None


def ask(message: str) -> Dict[str, Any]:
    result = _graph(message)
    results: Dict[str, str] = {}
    for node_id, node_result in getattr(result, "results", {}).items():
        results[node_id] = _result_text(node_result)

    orchestrator_payload = None
    orchestrator_text = results.get("orchestrator", "")
    if orchestrator_text:
        orchestrator_payload = _parse_json(orchestrator_text)

    sections = []
    query = None
    if orchestrator_payload and "query" in orchestrator_payload:
        query = str(orchestrator_payload["query"])
        sections.append(f"Query: {query}")

    flight_text = results.get("flight_search")
    hotel_text = results.get("hotel_search")
    flights = _parse_json(flight_text) if flight_text else None
    hotels = _parse_json(hotel_text) if hotel_text else None
    if flights:
        sections.append("Flights:\n" + json.dumps(flights, indent=2))
    elif flight_text:
        sections.append("Flights:\n" + flight_text)
    if hotels:
        sections.append("Hotels:\n" + json.dumps(hotels, indent=2))
    elif hotel_text:
        sections.append("Hotels:\n" + hotel_text)

    if sections:
        answer = "\n\n".join(sections)
    elif orchestrator_text:
        answer = orchestrator_text
    else:
        answer = "\n\n".join(text for text in results.values() if text)

    return {
        "answer": answer or "",
        "query": query,
        "orchestrator": orchestrator_payload,
        "flights": flights,
        "hotels": hotels,
        "status": _json_safe(getattr(result, "status", None)),
        "execution_time_ms": getattr(result, "execution_time", None),
        "execution_order": [
            getattr(node, "node_id", None)
            for node in getattr(result, "execution_order", [])
        ],
        "results": results,
    }


@app.post("/chat")
def chat(req: ChatRequest) -> Dict[str, Any]:
    return ask(req.message)


def _mount_ui(app: FastAPI) -> Optional[Path]:
    root_dir = Path(__file__).resolve().parents[2]
    ui_dir = root_dir / "ui"
    if ui_dir.exists():
        app.mount("/ui", StaticFiles(directory=str(ui_dir), html=True), name="ui")
        return ui_dir
    return None


_mount_ui(app)


def main() -> None:
    import uvicorn

    host = os.getenv("TRAVEL_AGENT_HOST", "127.0.0.1")
    port = int(os.getenv("TRAVEL_AGENT_PORT", "8000"))
    reload_flag = os.getenv("TRAVEL_AGENT_RELOAD", "true").lower() in {"1", "true", "yes"}
    uvicorn.run("travel_agent.server:app", host=host, port=port, reload=reload_flag)
