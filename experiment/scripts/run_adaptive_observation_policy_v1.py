import argparse,json,hashlib
from pathlib import Path
from pnp_architecture.adaptive_observation_policy_v1 import experiment
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path,required=True);a=p.parse_args();r=experiment();r['protocol_sha256']=hashlib.sha256((ROOT/'experiment/docs/protocol-adaptive-observation-policy-v1.md').read_bytes()).hexdigest();r['source_sha256']=hashlib.sha256((ROOT/'experiment/src/pnp_architecture/adaptive_observation_policy_v1.py').read_bytes()).hexdigest();a.output.open('x').write(json.dumps(r,sort_keys=True,indent=2)+'\n');b=r['best_policy'];text='# Adaptive observation-policy v1\n\n| Policy | Cost | Identifiable |\n|---|---:|---|\n| passive | 0 | %s |\n| local_parity + local_group | %d | %s |\n| privileged_exact | 6 | True |\n\nBest finite policy: `%s`, cost %d. Values are synthetic modeled units.\n'%(r['passive_identifiable'],b['cost'],b['identifiable'],' -> '.join(b['actions']),b['cost']);a.summary.open('x').write(text);print(text)
if __name__=='__main__':main()
