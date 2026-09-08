#!/usr/bin/env python3
"""Execute frozen release-v1 cells locally; refuse all output overwrites."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from pnp_architecture import release


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prefix', type=Path, required=True)
    args = parser.parse_args()
    paths = [Path(str(args.prefix) + suffix) for suffix in ('.json', '.md')]
    if any(p.exists() for p in paths):
        parser.error('refusing overwrite: output already exists')
    protocol = ROOT / 'docs/protocol-release-v1.md'
    protocol_hash = hashlib.sha256(protocol.read_bytes()).hexdigest()
    if protocol_hash != Path(str(protocol)+'.sha256').read_text().split()[0]:
        raise RuntimeError('frozen protocol hash mismatch')
    expected = (ROOT/'src/pnp_architecture/release.py').resolve()
    if Path(release.__file__).resolve() != expected:
        raise RuntimeError('unexpected imported release module')
    sources = ['src/pnp_architecture/release.py', 'scripts/run_release.py',
               'tests/test_release.py', 'docs/protocol-release-v1.md',
               'docs/protocol-release-v1.md.sha256']
    fixtures = [release.materialize(cell) for cell in release.cells()]
    rows = [release.evaluate(fixture, policy) for fixture in fixtures for policy in release.POLICIES]
    for row in rows:
        if row['policy'] in release.SAFE and row['decisions'] != row['oracle']:
            raise AssertionError(f"safe policy diverged: {row['cell']} {row['policy']}")
    receipt = dict(schema='release-v1', trust='TRUSTED ATTESTATION; public lab HMAC key; not proof of truth',
                   provenance=dict(module_path=str(expected), protocol_sha256=protocol_hash,
                                   sha256={p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources}),
                   fixtures=fixtures, rows=rows)
    content = [(json.dumps(receipt, sort_keys=True, indent=2)+'\n').encode(), release.summary(receipt).encode()]
    for p, data in zip(paths, content):
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('xb') as stream:
            stream.write(data)
    if json.loads(paths[0].read_bytes()) != receipt or paths[1].read_bytes() != content[1]:
        raise RuntimeError('output readback mismatch')
    print(f"{len(fixtures)} cells; {len(rows)} rows; safe exact equivalence verified")
    for p in paths:
        print(f"{p}: {p.stat().st_size} bytes sha256={hashlib.sha256(p.read_bytes()).hexdigest()}")


if __name__ == '__main__':
    main()
