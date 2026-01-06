import os
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from travel_agent.app import build_graph

app = FastAPI()

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


def ask(message: str) -> Dict[str, Any]:
    result = _graph(message)
    results: Dict[str, str] = {}
    for node_id, node_result in getattr(result, "results", {}).items():
        results[node_id] = _result_text(node_result)

    answer = results.get("orchestrator")
    if not answer:
        answer = "\n\n".join(text for text in results.values() if text)

    return {
        "answer": answer or "",
        "status": _json_safe(getattr(result, "status", None)),
        "execution_time_ms": getattr(result, "execution_time", None),
        "results": results,
    }


@app.on_event("startup")
def _startup() -> None:
    global _graph
    _graph = build_graph()


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
