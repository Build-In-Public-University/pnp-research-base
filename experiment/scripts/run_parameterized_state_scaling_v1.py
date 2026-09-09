import argparse,hashlib,json
from pathlib import Path
from pnp_architecture.parameterized_state_scaling_v1 import experiment
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path,required=True);a=p.parse_args()
 if a.output.exists() or a.summary.exists() or a.output.resolve()==a.summary.resolve():raise SystemExit('output paths must be new and distinct')
 r=experiment(range(1,9));r['protocol_sha256']=hashlib.sha256((ROOT/'experiment/docs/protocol-parameterized-contract-state-scaling-v1.md').read_bytes()).hexdigest();r['source_sha256']=hashlib.sha256((ROOT/'experiment/src/pnp_architecture/parameterized_state_scaling_v1.py').read_bytes()).hexdigest()
 a.output.parent.mkdir(parents=True,exist_ok=True);a.summary.parent.mkdir(parents=True,exist_ok=True);a.output.open('x').write(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
 lines=['# Parameterized contract-state scaling v1','','| n | K_G | I_G bits | Pairwise | Max depth | Update | Decision |','|---:|---:|---:|---|---:|---:|---:|']
 for x in r['rows']:lines.append('| %d | %d | %d | %s | %d | %d | %d |'%(x['n'],x['K_G'],x['I_G_bits'],x['all_pairwise_distinguishable'],x['max_distinguishing_depth'],x['update_work_per_event'],x['decision_work_per_query']))
 text='\n'.join(lines)+'\n\nThe family receipt separates exponential semantic-state count from linear information bits, constant modeled bit-update work, and linear decision scan work.\n';a.summary.open('x').write(text);print(text)
if __name__=='__main__':main()
