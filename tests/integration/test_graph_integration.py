import os

import jsonschema
import pytest

from travel_agent.app import build_graph
from travel_agent.server import _parse_json, _result_text
from tests.travel_agent.contract.schemas import FLIGHT_SCHEMA, HOTEL_SCHEMA


@pytest.mark.integration
def test_graph_returns_flights_and_hotels():
    graph = build_graph()
    result = graph(
        "Plan a trip from SFO to LAX on 2025-01-10 with flights and hotels."
    )
    results = getattr(result, "results", {})
    flights = _parse_json(_result_text(results.get("flight_search")))
    hotels = _parse_json(_result_text(results.get("hotel_search")))

    assert flights is not None, "Expected flight results."
    assert hotels is not None, "Expected hotel results."

    jsonschema.validate(flights, FLIGHT_SCHEMA)
    jsonschema.validate(hotels, HOTEL_SCHEMA)
