import json
from pathlib import Path

from .model import receipt


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Run the first synthetic P/NP architecture attack")
    parser.add_argument("--output", default="artifacts/first_attack.json")
    args = parser.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    data = receipt()
    output.write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps({"status": data["status"], "rows": len(data["rows"]), "output": str(output)}))


if __name__ == "__main__":
    main()
