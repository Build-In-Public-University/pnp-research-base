import argparse,json,hashlib
from pathlib import Path
from pnp_architecture.capability_placement_freshness_v1 import experiment
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path,required=True);a=p.parse_args();r=experiment();r['protocol_sha256']=hashlib.sha256((ROOT/'experiment/docs/protocol-capability-placement-freshness-v1.md').read_bytes()).hexdigest();r['source_sha256']=hashlib.sha256((ROOT/'experiment/src/pnp_architecture/capability_placement_freshness_v1.py').read_bytes()).hexdigest();a.output.open('x').write(json.dumps(r,sort_keys=True,indent=2)+'\n');text='# Capability placement freshness v1\n\n| lambda | n=1 best | n=4 best | n=12 best |\n|---:|---|---|---|\n';
 for lam in r['lambdas']:
  rows=[x for x in r['rows'] if x['lambda']==lam];text+=f"| {lam} | {rows[0]['best']} | {rows[3]['best']} | {rows[11]['best']} |\n"
 a.summary.open('x').write(text);print(text)
if __name__=='__main__':main()
