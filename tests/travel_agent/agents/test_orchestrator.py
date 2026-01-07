from travel_agent.agents import OrchestratorAgent


def test_orchestrator_prompt_contract():
    agent = OrchestratorAgent().build()
    prompt = agent.system_prompt
    assert "JSON" in prompt
    assert "currency" in prompt
    assert "EUR" in prompt
    assert "No prose" in prompt or "JSON only" in prompt
