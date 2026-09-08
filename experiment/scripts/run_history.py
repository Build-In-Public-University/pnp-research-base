"""Run history experiment with fixed protocol, exclusive outputs, full receipts."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from pnp_architecture import history as history_module
from pnp_architecture.history import experiment

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ['docs/protocol-history-v1.md', 'src/pnp_architecture/history.py',
           'scripts/run_history.py', 'tests/test_history.py',
           'docs/protocol-history-v1.1.md', 'tests/test_history_properties.py']


def summary(receipt):
    cells = receipt['cells']
    lines = ['# History experiment v1.1: corrected executed results', '',
             'Costs: listed unit-weight operation counters, NOT time or physical energy.',
             'World/input generation, feed production and oracle/serialization work excluded.',
             '', '## Representative seed 1, n=64 (initial setup + 32 updates)', '',
             '| Changed inputs per step | Feed | Cold ops/errors | Snapshot ops/errors | Unchecked ops/errors | Feed repair ops/errors |',
             '|---|---|---|---|---|---|']
    for cell in cells:
        if cell['n'] == 64 and cell['seed'] == 1:
            vals = [f"{cell['policies'][name]['operations']}/{cell['policies'][name]['wrong_outputs']}"
                    for name in ('cold', 'incremental_snapshot', 'unchecked', 'incremental_feed')]
            lines.append(f"| {cell['updates_per_step']} | {cell['visibility']} | " + ' | '.join(vals) + ' |')
    lines += ['', 'Errors mean wrong returned vector/total/decision; not necessarily false acceptance.',
              '', '## Paired exact-policy outcomes (complete-feed cells only to avoid duplicate worlds)', '']
    for n in (16,64):
        for k in (0,1,n//4,n):
            selected = [c for c in cells if c['n']==n and c['updates_per_step']==k and c['visibility']=='complete']
            outcomes = Counter('snapshot_wins' if c['policies']['incremental_snapshot']['operations'] < c['policies']['cold']['operations']
                               else 'cold_wins' if c['policies']['incremental_snapshot']['operations'] > c['policies']['cold']['operations']
                               else 'tie' for c in selected)
            lines.append(f'- n={n}, changes={k}: {dict(outcomes)} across three seeds.')
    lines += ['', '## Safety totals (cell-step observations, NOT independent population samples)', '']
    for visibility in ('complete','omitted'):
        for policy in ('cold', 'incremental_snapshot', 'unchecked', 'incremental_feed'):
            pp = [c['policies'][policy] for c in cells if c['visibility']==visibility]
            lines.append(f"- {visibility}, {policy}: wrong outputs={sum(p['wrong_outputs'] for p in pp)}, "
                         f"false accepts={sum(p['false_acceptances'] for p in pp)}, false rejects={sum(p['false_rejections'] for p in pp)}.")
    lines += ['', '## Priced consequence winners (all cells; ties credited to every winner)', '',
              'Synthetic price per wrong output; no implied permission to violate correctness.']
    for penalty in receipt['penalties']:
        counts = Counter()
        for c in cells:
            row = next(r for r in c['surface']['rows'] if r['penalty_per_wrong_output']==penalty)
            counts.update(row['winners'])
        lines.append(f'- penalty={penalty}: {dict(counts)}')
    strict_counts = Counter()
    for cell in cells:
        strict_counts.update(cell['surface']['strict_correctness_winners'])
    lines += ['', '## Strict observed-correctness winners (all cells)', '',
              str(dict(strict_counts)),
              '', 'Each cell stores an exact rational break-even price against its cheapest observed-exact policy.',
              'Observed-exact eligibility is retrospective for this trajectory, not a guarantee for future inputs.',
              'Cells sharing a trajectory or differing only in feed visibility are paired, not independent evidence.',
              'No universal winner, dynamic solver optimality, physical cost, AI effect, or P/NP inference follows.']
    return '\n'.join(lines)+'\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--summary', type=Path, required=True)
    args = parser.parse_args()
    if Path(history_module.__file__).resolve() != (ROOT/'src/pnp_architecture/history.py').resolve():
        raise SystemExit('Imported history module does not match this checkout')
    if args.output.resolve() == args.summary.resolve():
        raise SystemExit('Output and summary must be distinct')
    if args.output.exists() or args.summary.exists():
        raise SystemExit('Refusing to overwrite retained artifact')
    hashes = {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCES}
    if hashes[SOURCES[0]] != (ROOT/'docs/protocol-history-v1.sha256').read_text().strip():
        raise SystemExit('Frozen protocol drift')
    if hashes['docs/protocol-history-v1.1.md'] != (ROOT/'docs/protocol-history-v1.1.sha256').read_text().strip():
        raise SystemExit('Frozen review amendment drift')
    receipt = experiment()
    receipt['revision'] = '1.1'
    receipt['module_provenance'] = 'resolved imported module verified against checkout before execution'
    receipt['source_sha256'] = hashes
    # Compact serialization: all inputs/results retained without whitespace inflation.
    with args.output.open('x') as f:
        f.write(json.dumps(receipt,sort_keys=True,separators=(',',':'))+'\n')
    text = summary(receipt)
    with args.summary.open('x') as f:
        f.write(text)
    print('Executed cells:', len(receipt['cells']))
    print(text)


if __name__ == '__main__':
    main()
