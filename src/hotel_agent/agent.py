from dataclasses import dataclass
from typing import Optional

from strands import Agent
from strands.models.ollama import OllamaModel


@dataclass
class HotelSearchAgent:
    def build(self, model: Optional[OllamaModel] = None) -> Agent:
        return Agent(
            name="hotel_search",
            model=model,
            system_prompt=(
                "You search hotels. Return ONLY a JSON array of exactly 3 hotel objects. "
                "Schema: {name: string, city: string, checkout: string, "
                "price_per_night: number, currency: string}. Currency must be EUR by default "
                "and must match the customer's requested currency if specified. "
                "No prose, no markdown, JSON only."
            ),
        )
