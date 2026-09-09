"""Run dynamic dependency repair v1 with exclusive, provenance-bearing outputs."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from pnp_architecture import dynamic as dynamic_module
from pnp_architecture.dynamic import experiment

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    "docs/protocol-dynamic-dependencies-v1.md",
    "src/pnp_architecture/dynamic.py",
    "scripts/run_dynamic.py",
    "tests/test_dynamic.py",
]


def summarize(receipt):
    cells = receipt["cells"]
    totals = Counter()
    winners = Counter()
    for cell in cells:
        for policy, result in cell["policies"].items():
            totals[policy] += result["operations"]
        correct = [p for p, r in cell["policies"].items() if r["wrong_outputs"] == 0]
        if correct:
            best = min(cell["policies"][p]["operations"] for p in correct)
            winners.update(p for p in correct if cell["policies"][p]["operations"] == best)
    lines = [
        "# Dynamic dependency repair v1: executed results",
        "",
        "Listed logical operation counters, not runtime, energy, money, or hardware measurements.",
        f"Cells: {len(cells)}; policies: {', '.join(receipt['policies'])}.",
        "",
        "## Aggregate policy totals",
        "",
        "| Policy | Operations | Wrong outputs | Stale acceptances |",
        "|---|---:|---:|---:|",
    ]
    for policy in receipt["policies"]:
        rows = [c["policies"][policy] for c in cells]
        lines.append(f"| {policy} | {sum(r['operations'] for r in rows)} | {sum(r['wrong_outputs'] for r in rows)} | {sum(r['stale_acceptances'] for r in rows)} |")
    lines += [
        "",
        "## Strict exactness winners",
        "",
        str(dict(winners)),
        "",
        "A strict winner is the least-operation policy among policies that were exact on that cell. Cells are paired by generated seed and are not independent population samples.",
        "",
        "## Interpretation boundary",
        "",
        "The certificate policy is a modeled validation channel, not cryptographic proof of semantic truth. Hidden drift is synthetic. These finite runs test dependency repair and stale-state accounting; they establish no dynamic lower bound, deployment result, or P/NP claim.",
    ]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    if Path(dynamic_module.__file__).resolve() != (ROOT / "src/pnp_architecture/dynamic.py").resolve():
        raise SystemExit("Imported dynamic module does not match this checkout")
    if args.output.resolve() == args.summary.resolve():
        raise SystemExit("Output and summary must be distinct")
    if args.output.exists() or args.summary.exists():
        raise SystemExit("Refusing to overwrite existing artifact")
    protocol = ROOT / SOURCES[0]
    protocol_hash = hashlib.sha256(protocol.read_bytes()).hexdigest()
    if protocol_hash != (ROOT / "docs/protocol-dynamic-dependencies-v1.sha256").read_text().strip():
        raise SystemExit("Frozen protocol drift")
    hashes = {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in SOURCES}
    receipt = experiment()
    receipt["revision"] = "1"
    receipt["protocol_sha256"] = protocol_hash
    receipt["source_sha256"] = hashes
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.output.open("x").write(json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n")
    args.summary.open("x").write(summarize(receipt))
    print(summarize(receipt))


if __name__ == "__main__":
    main()
