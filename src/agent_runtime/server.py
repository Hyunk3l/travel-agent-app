import importlib
import os
from typing import Any, Callable, Optional

from fastapi import FastAPI
from pydantic import BaseModel
from strands import Agent
from strands.models.ollama import OllamaModel


class InvokeRequest(BaseModel):
    message: str


def extract_text(node_result: Any) -> str:
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


def build_model() -> OllamaModel:
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    model_id = os.getenv("OLLAMA_MODEL", "llama3.1")
    return OllamaModel(host=host, model_id=model_id)


def create_app(
    agent_factory: Callable[[Optional[OllamaModel]], Agent],
    model: Optional[OllamaModel] = None,
) -> FastAPI:
    if model is None:
        model = build_model()
    agent = agent_factory(model)

    app = FastAPI()

    @app.post("/invoke")
    def invoke(req: InvokeRequest) -> dict:
        result = agent(req.message)
        return {"output": extract_text(result)}

    return app


def load_agent_factory() -> Callable[[Optional[OllamaModel]], Agent]:
    value = os.getenv("AGENT_CLASS", "").strip()
    if not value:
        raise RuntimeError("AGENT_CLASS is required (e.g. flight_agent.agent:FlightSearchAgent).")

    module_name, _, class_name = value.partition(":")
    if not module_name or not class_name:
        raise RuntimeError("AGENT_CLASS must look like module:ClassName.")

    module = importlib.import_module(module_name)
    agent_class = getattr(module, class_name)
    return agent_class().build


def get_app() -> FastAPI:
    return create_app(load_agent_factory())


def main() -> None:
    import uvicorn

    host = os.getenv("AGENT_HOST", "0.0.0.0")
    port = int(os.getenv("AGENT_PORT", "8080"))
    uvicorn.run(get_app(), host=host, port=port)


if __name__ == "__main__":
    main()
