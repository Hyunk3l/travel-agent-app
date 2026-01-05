import argparse
import json
from typing import Any, Dict

from travel_agent.app import build_graph


def _result_text(node_result: Any) -> str:
    result = getattr(node_result, "result", None)
    message = getattr(result, "message", None) if result else None
    content = getattr(message, "content", None) if message else None
    if content:
        chunks = []
        for block in content:
            text = getattr(block, "text", None)
            if text:
                chunks.append(text)
        if chunks:
            return "\n".join(chunks)
    return str(result) if result is not None else ""


def _json_safe(value: Any) -> Any:
    if value is None:
        return None
    enum_value = getattr(value, "value", None)
    if enum_value is not None:
        return enum_value
    return str(value)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Travel agent demo.")
    parser.add_argument("--origin", default=None, help="Origin airport or city.")
    parser.add_argument("--destination", default=None, help="Destination airport or city.")
    parser.add_argument("--depart", default=None, help="Departure date (YYYY-MM-DD).")
    parser.add_argument("--return", dest="return_date", default=None, help="Return date (YYYY-MM-DD).")
    parser.add_argument("--flight", action="store_true", help="Include flight search.")
    parser.add_argument("--hotel", action="store_true", help="Include hotel search.")
    return parser.parse_args()


def build_state(args: argparse.Namespace) -> Dict[str, Any]:
    parts = []
    if args.origin and args.destination:
        parts.append(f"{args.origin} to {args.destination}")
    if args.depart:
        parts.append(f"depart {args.depart}")
    if args.return_date:
        parts.append(f"return {args.return_date}")
    if args.hotel and args.flight:
        parts.append("flights and hotels")
    elif args.hotel and not args.flight:
        parts.append("hotel only")
    elif args.flight and not args.hotel:
        parts.append("flight only")

    return {"request": ", ".join(parts) if parts else "Plan a trip."}


def main() -> None:
    args = parse_args()
    state = build_state(args)
    graph = build_graph()
    result = graph(state["request"])
    output: Dict[str, Any] = {
        "status": _json_safe(getattr(result, "status", None)),
        "execution_time_ms": getattr(result, "execution_time", None),
        "execution_order": [
            getattr(node, "node_id", None)
            for node in getattr(result, "execution_order", [])
        ],
        "results": {},
    }

    for node_id, node_result in getattr(result, "results", {}).items():
        output["results"][node_id] = _result_text(node_result)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
