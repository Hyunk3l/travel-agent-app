import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert JSON eval cases to JSONL for Eval SOP."
    )
    parser.add_argument(
        "--input",
        default="tests/eval/test_cases.json",
        help="Path to JSON test cases file.",
    )
    parser.add_argument(
        "--output",
        default="eval/test-cases.jsonl",
        help="Path to JSONL output file.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with input_path.open("r", encoding="utf-8") as handle:
        cases = json.load(handle)

    with output_path.open("w", encoding="utf-8") as handle:
        for case in cases:
            handle.write(json.dumps(case, ensure_ascii=True) + "\n")

    print(f"Wrote {len(cases)} cases to {output_path}")


if __name__ == "__main__":
    main()
