import argparse,json,hashlib
from pathlib import Path
from pnp_architecture.interactive_observation_policy_v1 import experiment
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path,required=True);a=p.parse_args();r=experiment();r['protocol_sha256']=hashlib.sha256((ROOT/'experiment/docs/protocol-interactive-observation-policy-v1.md').read_bytes()).hexdigest();r['source_sha256']=hashlib.sha256((ROOT/'experiment/src/pnp_architecture/interactive_observation_policy_v1.py').read_bytes()).hexdigest();a.output.open('x').write(json.dumps(r,sort_keys=True,indent=2)+'\n');lines=['# Interactive observation-policy v1','','| Policy | Identifiable | Observation cost | Perturbs system |','|---|---|---:|---|']
 for p,x in r['policies'].items():lines.append(f"| {p} | {x['identifiable']} | {x['observation_cost']} | {x['measurement_perturbation']} |")
 a.summary.open('x').write('\n'.join(lines)+'\n\nEnergy labels are synthetic; passive transcripts are identical across hidden states.\n');print(a.summary.read_text())
if __name__=='__main__':main()
