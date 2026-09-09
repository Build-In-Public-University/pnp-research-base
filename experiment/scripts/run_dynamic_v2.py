"""Run dynamic dependency consequence v2 with exclusive receipts."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from pnp_architecture import dynamic_v2 as module
from pnp_architecture.dynamic_v2 import CONSEQUENCE_PENALTIES, experiment

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    "docs/protocol-dynamic-dependencies-v2.md",
    "src/pnp_architecture/dynamic_v2.py",
    "src/pnp_architecture/dynamic.py",
    "scripts/run_dynamic_v2.py",
    "tests/test_dynamic_v2.py",
]


def summary(receipt):
    cells = receipt["cells"]
    totals = Counter()
    for c in cells:
        for policy, r in c["policies"].items():
            totals[policy] += r["total_cost"]
    break_even = Counter()
    for c in cells:
        for row in c["surface"]["rows"]:
            for winner in row["winners"]:
                break_even[(row["penalty"], winner)] += 1
    lines = [
        "# Dynamic dependency consequence v2: executed results", "",
        f"Cells: {len(cells)}; policies: {', '.join(receipt['policies'])}.",
        "Costs below use the declared default stale-failure rate and downstream penalty.",
        "Counters and consequence penalties are synthetic logical units, not runtime, energy, money, or incident probabilities.", "",
        "## Aggregate total modeled cost", "",
        "| Policy | Total modeled cost | Wrong outputs | Unsafe reuse | Stale failures |", "|---|---:|---:|---:|---:|",
    ]
    for policy in receipt["policies"]:
        rows = [c["policies"][policy] for c in cells]
        lines.append(f"| {policy} | {sum(r['total_cost'] for r in rows)} | {sum(r['wrong_outputs'] for r in rows)} | {sum(r['unsafe_reuse'] for r in rows)} | {sum(r['stale_failures'] for r in rows)} |")
    lines += ["", "## Break-even surface winner counts", "", "| Penalty | Policy wins/ties |", "|---:|---|",]
    for penalty in CONSEQUENCE_PENALTIES:
        entries = {p: break_even[(penalty, p)] for p in receipt["policies"] if break_even[(penalty, p)]}
        lines.append(f"| {penalty} | {entries} |")
    lines += ["", "A surface winner is a least-modeled-cost policy for that cell and penalty. Ties are credited to every tied policy.", "", "Certificate validation is a modeled input channel, not proof of semantic truth. Hidden drift, failure rates, and downstream penalties are synthetic. No P/NP or deployment claim follows."]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    if Path(module.__file__).resolve() != (ROOT / "src/pnp_architecture/dynamic_v2.py").resolve():
        raise SystemExit("Imported dynamic_v2 module does not match this checkout")
    if args.output.resolve() == args.summary.resolve() or args.output.exists() or args.summary.exists():
        raise SystemExit("Output paths must be distinct and new")
    protocol_hash = hashlib.sha256((ROOT / SOURCES[0]).read_bytes()).hexdigest()
    if protocol_hash != (ROOT / "docs/protocol-dynamic-dependencies-v2.sha256").read_text().strip():
        raise SystemExit("Frozen protocol drift")
    receipt = experiment()
    receipt["revision"] = "2"
    receipt["protocol_sha256"] = protocol_hash
    receipt["source_sha256"] = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in SOURCES}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.output.open("x").write(json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n")
    args.summary.open("x").write(summary(receipt))
    print(summary(receipt))


if __name__ == "__main__":
    main()
