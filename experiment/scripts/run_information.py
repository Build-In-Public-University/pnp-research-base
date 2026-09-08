"""Fresh-path deterministic runner for the finite information audit."""
import argparse
import hashlib
import json
from pathlib import Path
from pnp_architecture import information

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ('docs/protocol-information-v1.md', 'src/pnp_architecture/information.py',
           'scripts/run_information.py', 'tests/test_information.py')


def summary(receipt):
    return '\n'.join([
        '# Information-boundary finite audit v1', '',
        f"Binary contracts: {receipt['binary']}",
        f"Relational contracts with action constraints: {receipt['relational']}", '',
        'Pairwise intersecting acceptable-action sets can have empty joint intersection.',
        'Deferral resolves an ambiguity only if it is both contract-valid and feasible.',
        'States 48/49 need no distinction for <50; adding possible state 50 changes this.',
        'The declared compatible-world model is an assumption, not a free observation oracle.',
        receipt['boundary'], ''])


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--summary',type=Path,required=True)
    args=parser.parse_args()
    if Path(information.__file__).resolve() != (ROOT/'src/pnp_architecture/information.py').resolve():
        raise SystemExit('Imported module does not match checkout')
    if args.output.resolve()==args.summary.resolve() or args.output.exists() or args.summary.exists():
        raise SystemExit('Distinct fresh output paths required')
    hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCES}
    if hashes[SOURCES[0]] != (ROOT/'docs/protocol-information-v1.sha256').read_text().strip():
        raise SystemExit('Frozen protocol drift')
    result=information.experiment()
    result['source_sha256']=hashes
    text=summary(result)
    with args.output.open('x') as f:f.write(json.dumps(result,sort_keys=True,indent=2)+'\n')
    with args.summary.open('x') as f:f.write(text)
    print(text)

if __name__=='__main__':
    main()
