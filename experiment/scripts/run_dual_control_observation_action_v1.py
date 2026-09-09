import argparse,json,hashlib
from pathlib import Path
from pnp_architecture.dual_control_observation_action_v1 import experiment
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path,required=True);a=p.parse_args();r=experiment();r['protocol_sha256']=hashlib.sha256((ROOT/'experiment/docs/protocol-dual-control-observation-action-v1.md').read_bytes()).hexdigest();r['source_sha256']=hashlib.sha256((ROOT/'experiment/src/pnp_architecture/dual_control_observation_action_v1.py').read_bytes()).hexdigest();a.output.open('x').write(json.dumps(r,sort_keys=True,indent=2)+'\n');text='# Dual-control observation/action v1\n\n| Scenario | Immediate | Inspect | Gentle touch | Best |\n|---|---:|---:|---:|---|\n'+''.join(f"| {n} | {x['values']['act_immediately']} | {x['values']['inspect_then_act']} | {x['values']['gentle_touch_then_act']} | {x['best_policy']} |\n" for n,x in r['scenarios'].items());a.summary.open('x').write(text);print(text)
if __name__=='__main__':main()
