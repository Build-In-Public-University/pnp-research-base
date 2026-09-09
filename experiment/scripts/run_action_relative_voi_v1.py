import argparse,json,hashlib
from pathlib import Path
from pnp_architecture.action_relative_voi_v1 import experiment
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path,required=True);a=p.parse_args();r=experiment();r['protocol_sha256']=hashlib.sha256((ROOT/'experiment/docs/protocol-action-relative-voi-v1.md').read_bytes()).hexdigest();r['source_sha256']=hashlib.sha256((ROOT/'experiment/src/pnp_architecture/action_relative_voi_v1.py').read_bytes()).hexdigest();a.output.open('x').write(json.dumps(r,sort_keys=True,indent=2)+'\n');text='# Action-relative VOI v1\n\n| Belief | Entropy (bits) | Perfect-info VOI | Touch | Inspect | Best |\n|---|---:|---:|---:|---:|---|\n'+''.join(f"| {x['p']} | {x['entropy_bits']:.12f} | {x['voi_perfect_information']} | {x['costs']['touch']} | {x['costs']['inspect']} | {x['best_policy']} |\n" for x in r['beliefs'].values());a.summary.open('x').write(text);print(text)
if __name__=='__main__':main()
