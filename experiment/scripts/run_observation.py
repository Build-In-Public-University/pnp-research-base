"""Run only the local prospective observation suite; exclusive deterministic receipts."""
import argparse
import hashlib
import json
from pathlib import Path
from pnp_architecture import observation

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ('docs/protocol-observation-v1.md', 'docs/protocol-observation-v1.sha256',
           'src/pnp_architecture/observation.py', 'scripts/run_observation.py',
           'tests/test_observation.py')


def verify_sources(module_path=None):
    actual = Path(observation.__file__ if module_path is None else module_path).resolve()
    expected = (ROOT/'src/pnp_architecture/observation.py').resolve()
    if actual != expected:
        raise ValueError('Imported observation module does not match this checkout')
    hashes = {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in SOURCES}
    frozen = (ROOT/'docs/protocol-observation-v1.sha256').read_text().split()[0]
    if hashes['docs/protocol-observation-v1.md'] != frozen:
        raise ValueError('Frozen protocol hash mismatch')
    return hashes


def write_exclusive(path, receipt):
    with Path(path).open('x', encoding='utf-8') as stream:
        stream.write(observation.canonical(receipt))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit('Refusing to overwrite retained artifact')
    hashes = verify_sources()
    receipt = observation.experiment()
    receipt['source_sha256'] = hashes
    receipt['import_verified'] = 'src/pnp_architecture/observation.py'
    write_exclusive(args.output, receipt)
    print(json.dumps({'output': str(args.output), 'worlds': len(receipt['worlds']),
                      'cells': len(receipt['cells']),
                      'sha256': hashlib.sha256(args.output.read_bytes()).hexdigest()}, sort_keys=True))


if __name__ == '__main__':
    main()
