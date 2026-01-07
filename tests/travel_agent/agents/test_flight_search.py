from travel_agent.agents import FlightSearchAgent


def test_flight_search_prompt_contract():
    agent = FlightSearchAgent().build()
    prompt = agent.system_prompt
    assert "JSON array" in prompt
    assert "price: number" in prompt
    assert "currency: string" in prompt
    assert "EUR" in prompt
    assert "JSON only" in prompt
