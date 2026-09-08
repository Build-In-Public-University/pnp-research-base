#!/usr/bin/env python3
"""Run the frozen v2 suite locally; refuse to overwrite any existing output."""
import argparse
import hashlib
import json
from pathlib import Path

from pnp_architecture.experiments_v2 import run_suite, summary_markdown


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='artifacts/experiments_v2.json')
    parser.add_argument('--summary', default='artifacts/experiments_v2-summary.md')
    args = parser.parse_args()
    output, summary = Path(args.output), Path(args.summary)
    if output.resolve() == summary.resolve():
        parser.error('JSON and summary paths must differ')
    for path in (output, summary):
        if path.exists():
            parser.error(f'refusing to overwrite existing output: {path}')
    root = Path(__file__).resolve().parents[1]
    data = run_suite(root)
    encoded = json.dumps(data, sort_keys=True, indent=2) + '\n'
    markdown = summary_markdown(data)
    for path, content in [(output, encoded), (summary, markdown)]:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('x') as stream:
            stream.write(content)
    print(json.dumps({'status': data['status'], 'graphs': len(data['graphs']),
                      'propagation_cells': len(data['propagation']),
                      'containing_witnesses': len(data['containing_constraint']),
                      'cnf_formulas': len(data['cnf']),
                      'receipt_sha256': hashlib.sha256(encoded.encode()).hexdigest(),
                      'output': str(output), 'summary': str(summary)}, sort_keys=True))


if __name__ == '__main__':
    main()
