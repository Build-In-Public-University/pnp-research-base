import argparse,json,hashlib
from pathlib import Path
from pnp_architecture.dual_control_policy_phase_diagram_v1 import experiment
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path,required=True);a=p.parse_args();r=experiment();r['protocol_sha256']=hashlib.sha256((ROOT/'experiment/docs/protocol-dual-control-policy-phase-diagram-v1.md').read_bytes()).hexdigest();r['source_sha256']=hashlib.sha256((ROOT/'experiment/src/pnp_architecture/dual_control_policy_phase_diagram_v1.py').read_bytes()).hexdigest();a.output.open('x').write(json.dumps(r,sort_keys=True,indent=2)+'\n');text='# Dual-control policy phase diagram v1\n\n| Region | Grid interval |\n|---|---|\n'+''.join(f'| {n} | [{lo}, {hi}] |\n' for n,lo,hi in r['intervals'])+'\nAnalytic thresholds: 1/90, 0.4, 0.95. Values are synthetic modeled costs.\n';a.summary.open('x').write(text);print(text)
if __name__=='__main__':main()
