# Travel Agent (Strands Graph Pattern)

This project demonstrates a minimal travel agent built with the Strands Agents
SDK and its "Graph pattern." The graph connects three agents:

- Orchestrator agent (routes the request)
- Flight search agent
- Hotel search agent

Install the SDK with Ollama support:

```bash
pip install 'strands-agents[ollama]'
```

Start Ollama and pull a model:

```bash
ollama serve
ollama pull llama3.1
```

## Quick start

```bash
python -m travel_agent --origin SFO --destination LAX --depart 2025-01-10 --return 2025-01-14 --hotel
```

Run from a local venv:

```bash
source .venv/bin/activate
pip install -e .
OLLAMA_HOST=http://localhost:11434 OLLAMA_MODEL=llama3.1 travel-agent --origin SFO --destination LAX --depart 2025-01-10
```

Or install and run:

```bash
pip install -e .
travel-agent --origin SFO --destination LAX --depart 2025-01-10 --return 2025-01-14 --hotel
```

You can override the Ollama host or model:

```bash
OLLAMA_HOST=http://localhost:11434 OLLAMA_MODEL=llama3.1 travel-agent --origin SFO --destination LAX --depart 2025-01-10
```

## What it does

- The orchestrator reads the request, sets flags for which searches to run, and
  builds a normalized query string.
- The graph conditionally fans out to the flight and hotel agents based on those
  flags.
- Results are merged back into a single response object.

## Project layout

- `src/travel_agent/app.py`: graph wiring (Strands GraphBuilder)
- `src/travel_agent/agents.py`: three agents (orchestrator, flight, hotel)
- `src/travel_agent/main.py`: CLI entry point
