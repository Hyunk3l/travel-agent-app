from travel_agent.agents import HotelSearchAgent


def test_hotel_search_prompt_contract():
    agent = HotelSearchAgent().build()
    prompt = agent.system_prompt
    assert "JSON array" in prompt
    assert "price_per_night: number" in prompt
    assert "currency: string" in prompt
    assert "EUR" in prompt
    assert "JSON only" in prompt
