import argparse
import csv
import json
import os
from datetime import datetime
from pathlib import Path
from time import perf_counter
from typing import Any, Dict, List

from travel_agent.app import build_graph
from travel_agent.server import _parse_json, _result_text


def load_cases(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def run_graph(graph, query: str) -> Dict[str, Any]:
    result = graph(query)
    results = getattr(result, "results", {})
    flights = _parse_json(_result_text(results.get("flight_search")))
    hotels = _parse_json(_result_text(results.get("hotel_search")))
    return {
        "status": getattr(result, "status", None),
        "execution_time_ms": getattr(result, "execution_time", None),
        "flights": flights,
        "hotels": hotels,
        "raw_results": {k: str(v) for k, v in results.items()},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate travel agents.")
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
    args = parser.parse_args()

    cases_path = Path(args.cases)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    cases = load_cases(cases_path)
    graph = build_graph()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_path = output_dir / f"graph_results_{timestamp}.csv"

    with results_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "id",
                "category",
                "query",
                "expected",
                "status",
                "elapsed_ms",
            ],
        )
        writer.writeheader()
        for case in cases:
            start = perf_counter()
            output = run_graph(graph, case["query"])
            elapsed_ms = round((perf_counter() - start) * 1000)
            writer.writerow(
                {
                    "id": case.get("id", ""),
                    "category": case.get("category", ""),
                    "query": case.get("query", ""),
                    "expected": case.get("expected", ""),
                    "status": output.get("status"),
                    "elapsed_ms": elapsed_ms,
                }
            )

    print(f"Saved results to {results_path}")


if __name__ == "__main__":
    main()
