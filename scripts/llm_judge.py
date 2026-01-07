import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from strands import Agent
from strands.models.ollama import OllamaModel

from travel_agent.app import build_graph


EVAL_PROMPT = """You are an expert AI evaluator. Your job is to assess the quality of AI responses based on:
1. Accuracy - factual correctness of the response
2. Relevance - how well the response addresses the query
3. Completeness - whether all aspects of the query are addressed
4. Tool usage - appropriate use of available tools
Score each criterion from 1-5, where 1 is poor and 5 is excellent. Provide an overall score and brief explanation."""


def load_cases(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    parser = argparse.ArgumentParser(description="LLM judge evaluation runner.")
    parser.add_argument(
        "--cases",
        default="tests/eval/test_cases.json",
        help="Path to JSON test cases file.",
    )
    parser.add_argument(
        "--output",
        default="evaluation_results",
        help="Directory for evaluation outputs.",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("EVAL_MODEL", "llama3.1"),
        help="Evaluator model ID.",
    )
    parser.add_argument(
        "--host",
        default=os.getenv("EVAL_OLLAMA_HOST", "http://localhost:11434"),
        help="Ollama host for evaluator model.",
    )
    args = parser.parse_args()

    cases_path = Path(args.cases)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    evaluator = Agent(
        model=OllamaModel(host=args.host, model_id=args.model),
        system_prompt=EVAL_PROMPT,
    )
    graph = build_graph()

    results = []
    for case in load_cases(cases_path):
        query = case["query"]
        agent_response = graph(query)
        eval_prompt = (
            "Query:\n"
            f"{query}\n\n"
            "Response to evaluate:\n"
            f"{agent_response}\n\n"
            "Expected response (if available):\n"
            f"{case.get('expected', 'Not provided')}\n"
        )
        evaluation = evaluator(eval_prompt)
        results.append(
            {
                "test_id": case.get("id", ""),
                "query": query,
                "agent_response": str(agent_response),
                "evaluation": str(evaluation),
            }
        )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"llm_judge_{timestamp}.json"
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(results, handle, indent=2)

    print(f"Saved LLM judge results to {output_path}")


if __name__ == "__main__":
    main()
