from dataclasses import dataclass
from typing import Optional

from strands import Agent
from strands.models.ollama import OllamaModel


@dataclass
class OrchestratorAgent:
    def build(self, model: Optional[OllamaModel] = None) -> Agent:
        return Agent(
            name="orchestrator",
            model=model,
            system_prompt=(
                "You are a travel request orchestrator. Read the user request and "
                "decide which services are needed. Reply with ONLY strict JSON like: "
                '{"needs_flight": true, "needs_hotel": false, "query": "...", "currency": "EUR"} '
                "where query is a normalized trip summary and currency defaults to EUR unless "
                "the user specifies another currency. No prose, no markdown, JSON only."
            ),
        )
