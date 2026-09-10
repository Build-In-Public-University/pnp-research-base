import argparse,json,hashlib
from pathlib import Path
from pnp_architecture.stochastic_morphology_switching_v1 import experiment
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path,required=True);a=p.parse_args();r=experiment();r['protocol_sha256']=hashlib.sha256((ROOT/'experiment/docs/protocol-stochastic-morphology-switching-v1.md').read_bytes()).hexdigest();r['source_sha256']=hashlib.sha256((ROOT/'experiment/src/pnp_architecture/stochastic_morphology_switching_v1.py').read_bytes()).hexdigest();a.output.open('x').write(json.dumps(r,sort_keys=True,indent=2)+'\n');text='# Stochastic morphology switching v1\n\n| Agent | Total | Operating | Transition | Switches | Regret vs best fixed | Remote periods | Local periods |\n|---|---:|---:|---:|---:|---:|---:|---:|\n'+''.join(f"| {k} | {v['cost']:.3f} | {v['operating_cost']:.3f} | {v['transition_cost']:.3f} | {v['switches']} | {v['regret_vs_best_fixed']:.3f} | {v['occupancy']['remote']} | {v['occupancy']['local']} |\n" for k,v in r['agents'].items());a.summary.open('x').write(text);print(text)
if __name__=='__main__':main()
