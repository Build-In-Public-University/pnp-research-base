import argparse,json,hashlib
from pathlib import Path
from pnp_architecture.capability_space_routing_v1 import experiment
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path,required=True);a=p.parse_args();r=experiment();r['start']=[r['start'][0],sorted(r['start'][1]),*r['start'][2:]];r['final_state']=[r['final_state'][0],sorted(r['final_state'][1]),*r['final_state'][2:]];r['protocol_sha256']=hashlib.sha256((ROOT/'experiment/docs/protocol-capability-space-routing-v1.md').read_bytes()).hexdigest();r['source_sha256']=hashlib.sha256((ROOT/'experiment/src/pnp_architecture/capability_space_routing_v1.py').read_bytes()).hexdigest();a.output.open('x').write(json.dumps(r,sort_keys=True,indent=2)+'\n');text='# Capability-space routing v1\n\nGoal: `{parity, group}`\n\nBest route: `'+ ' -> '.join(r['best_path'])+'`\n\nCost: '+str(r['best_cost'])+'\n\nReachable composite capability: '+str(r['capability_acquisition'])+'\n';a.summary.open('x').write(text);print(text)
if __name__=='__main__':main()
