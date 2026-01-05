import json
import os
from typing import Any, Dict

from strands.multiagent import GraphBuilder
from strands.multiagent.graph import GraphState
from strands.models.ollama import OllamaModel

from travel_agent.agents import FlightSearchAgent, HotelSearchAgent, OrchestratorAgent


def _extract_text(node_result: Any) -> str:
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


def _read_orchestrator_payload(state: GraphState) -> Dict[str, Any]:
    orchestrator_result = state.results.get("orchestrator")
    text = _extract_text(orchestrator_result)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text}


def _needs_flight(state: GraphState) -> bool:
    payload = _read_orchestrator_payload(state)
    if "needs_flight" in payload:
        return bool(payload["needs_flight"])
    return "flight" in payload.get("raw", "").lower()


def _needs_hotel(state: GraphState) -> bool:
    payload = _read_orchestrator_payload(state)
    if "needs_hotel" in payload:
        return bool(payload["needs_hotel"])
    return "hotel" in payload.get("raw", "").lower()


def _build_model() -> OllamaModel:
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    model_id = os.getenv("OLLAMA_MODEL", "llama3.1")
    return OllamaModel(host=host, model_id=model_id)


def build_graph():
    model = _build_model()
    builder = GraphBuilder()
    builder.add_node(OrchestratorAgent().build(model), "orchestrator")
    builder.add_node(FlightSearchAgent().build(model), "flight_search")
    builder.add_node(HotelSearchAgent().build(model), "hotel_search")

    builder.add_edge("orchestrator", "flight_search", condition=_needs_flight)
    builder.add_edge("orchestrator", "hotel_search", condition=_needs_hotel)

    builder.set_entry_point("orchestrator")
    return builder.build()
