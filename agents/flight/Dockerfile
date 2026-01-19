FROM python:3.11-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml README.md /app/
COPY src /app/src

RUN pip install --no-cache-dir .

ENV AGENT_CLASS=flight_agent.agent:FlightSearchAgent
ENV AGENT_PORT=8080

EXPOSE 8080

CMD ["python", "-m", "agent_runtime.server"]
