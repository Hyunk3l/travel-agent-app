import pytest

from agent_runtime.server import InvokeRequest, create_app, load_agent_factory


def test_create_app_invokes_agent():
    class DummyAgent:
        def __call__(self, message: str) -> str:
            return f"echo:{message}"

    def factory(_model):
        return DummyAgent()

    app = create_app(factory, model=object())
    route = next(route for route in app.router.routes if route.path == "/invoke")
    response = route.endpoint(InvokeRequest(message="hello"))

    assert response == {"output": "echo:hello"}


def test_load_agent_factory_requires_env(monkeypatch):
    monkeypatch.delenv("AGENT_CLASS", raising=False)
    with pytest.raises(RuntimeError):
        load_agent_factory()


def test_load_agent_factory_accepts_module_path(monkeypatch):
    monkeypatch.setenv("AGENT_CLASS", "flight_agent.agent:FlightSearchAgent")
    factory = load_agent_factory()
    assert callable(factory)
