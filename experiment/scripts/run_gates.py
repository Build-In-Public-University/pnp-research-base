"""Run deterministic gate pilot to a fresh path; rejects protocol drift."""
import argparse
import hashlib
import json
from pathlib import Path
from pnp_architecture.gates import experiment

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ['docs/protocol-gates-v1.md', 'src/pnp_architecture/gates.py',
           'scripts/run_gates.py', 'tests/test_gates.py']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in SOURCES}
    if hashes[SOURCES[0]] != (ROOT / 'docs/protocol-gates-v1.sha256').read_text().strip():
        raise SystemExit('Frozen protocol drift')
    receipt = experiment()
    receipt['source_sha256'] = hashes
    # Exclusive creation prevents accidental replacement of a retained receipt.
    with args.output.open('x') as f:
        f.write(json.dumps(receipt, sort_keys=True, indent=2) + '\n')
    print('workload | cheap-first | composition-first | full-checks | accepted')
    for w in receipt['workloads']:
        print(w['name'], *(p['modeled_cost'] for p in w['policies']), w['policies'][0]['accepted'])
    print(json.dumps(receipt['transfer'], sort_keys=True))


if __name__ == '__main__':
    main()
