from dataclasses import dataclass
from typing import Optional

from strands import Agent
from strands.models.ollama import OllamaModel


@dataclass
class FlightSearchAgent:
    def build(self, model: Optional[OllamaModel] = None) -> Agent:
        return Agent(
            name="flight_search",
            model=model,
            system_prompt=(
                "You search flights. Return ONLY a JSON array of exactly 3 flight objects. "
                "Schema: {carrier: string, flight: string, route: string, depart: string, "
                "return: string, price: number, currency: string}. Currency must be EUR by "
                "default and must match the customer's requested currency if specified. "
                "No prose, no markdown, JSON only."
            ),
        )
