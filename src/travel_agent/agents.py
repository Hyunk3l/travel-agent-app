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
