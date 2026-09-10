import argparse
import hashlib
import json
from pathlib import Path
from pnp_architecture.adaptive_morphology_hysteresis_v1 import experiment
ROOT=Path(__file__).resolve().parents[2]
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path,required=True);a=p.parse_args()
    r=experiment()
    r['switch_costs']={f'{k[0]}->{k[1]}':v for k,v in r['switch_costs'].items()}
    r['protocol_sha256']=hashlib.sha256((ROOT/'experiment/docs/protocol-adaptive-morphology-hysteresis-v1.md').read_bytes()).hexdigest()
    r['source_sha256']=hashlib.sha256((ROOT/'experiment/src/pnp_architecture/adaptive_morphology_hysteresis_v1.py').read_bytes()).hexdigest()
    a.output.open('x').write(json.dumps(r,sort_keys=True,indent=2)+'\n')
    text='# Adaptive morphology hysteresis v1\n\n| demand | remote start | local start |\n|---:|---|---|\n'
    for d in [0,.1,.25,.5,1,2,2.25,3,4,8]:
        text+=f"| {d} | {next(x['policy'][0] for x in r['rows'] if x['d']==d and x['start']=='remote')} | {next(x['policy'][0] for x in r['rows'] if x['d']==d and x['start']=='local')} |\n"
    a.summary.open('x').write(text);print(text)
if __name__=='__main__':main()
