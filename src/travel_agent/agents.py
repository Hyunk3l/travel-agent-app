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
                "decide which services are needed. Reply with strict JSON like: "
                '{"needs_flight": true, "needs_hotel": false, "query": "..."} '
                "where query is a normalized trip summary."
            ),
        )


@dataclass
class FlightSearchAgent:
    def build(self, model: Optional[OllamaModel] = None) -> Agent:
        return Agent(
            name="flight_search",
            model=model,
            system_prompt=(
                "You search flights. Given the request, return a JSON array of "
                "3 flight options with keys: carrier, flight, route, depart, "
                "return, price_usd."
            ),
        )


@dataclass
class HotelSearchAgent:
    def build(self, model: Optional[OllamaModel] = None) -> Agent:
        return Agent(
            name="hotel_search",
            model=model,
            system_prompt=(
                "You search hotels. Given the request, return a JSON array of "
                "3 hotel options with keys: name, city, checkout, price_usd_per_night."
            ),
        )
