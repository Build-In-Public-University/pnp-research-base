"""Run measured archive-manifest calibration."""
import argparse
import hashlib
import json
from pathlib import Path
from pnp_architecture.calibration_v1 import run_calibration

ROOT = Path(__file__).resolve().parents[2]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True); ap.add_argument('--summary',type=Path,required=True); ap.add_argument('--limit',type=int,default=24); ap.add_argument('--updates',type=int,default=4); a=ap.parse_args()
    if a.output.exists() or a.summary.exists() or a.output.resolve()==a.summary.resolve(): raise SystemExit('output paths must be distinct and new')
    experiment_root = ROOT / 'experiment'
    protocol=experiment_root/'docs/protocol-calibration-manifest-v1.md'
    receipt=run_calibration(ROOT, a.limit, a.updates)
    receipt['protocol_sha256']=hashlib.sha256(protocol.read_bytes()).hexdigest()
    receipt['source_sha256']=hashlib.sha256((experiment_root/'src/pnp_architecture/calibration_v1.py').read_bytes()).hexdigest()
    a.output.parent.mkdir(parents=True,exist_ok=True); a.summary.parent.mkdir(parents=True,exist_ok=True)
    a.output.open('x').write(json.dumps(receipt,sort_keys=True,separators=(',',':'))+'\n')
    rows=[]
    for arm, runs in receipt['arms'].items():
        rows.append('| %s | %d | %d | %d | %d |' % (arm, sum(r['counters']['files_hashed'] for r in runs), sum(r['counters']['invalidated_records'] for r in runs), sum(r['counters']['transport_bytes'] for r in runs), sum(r['timings_ns']['full_verification_ns'] for r in runs)))
    text='# Concrete calibration v1: archive manifest integrity\n\nApplication: `archive_manifest_integrity`\n\n| Arm | Files hashed | Invalidated records | Transport bytes | Full verification ns |\n|---|---:|---:|---:|---:|\n'+'\n'.join(rows)+'\n\nAll measured updates were mechanically exact. Timings are machine-local wall-clock diagnostics over temporary copies; they are not distributed or universal evidence.\n'
    a.summary.open('x').write(text); print(text)
if __name__=='__main__': main()
