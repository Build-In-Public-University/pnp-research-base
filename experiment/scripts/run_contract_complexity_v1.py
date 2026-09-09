import argparse,hashlib,json
from pathlib import Path
from pnp_architecture.contract_complexity_v1 import experiment
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path,required=True);a=p.parse_args()
 if a.output.exists() or a.summary.exists() or a.output.resolve()==a.summary.resolve():raise SystemExit('output paths must be new and distinct')
 r=experiment(6);r['protocol_sha256']=hashlib.sha256((ROOT/'experiment/docs/protocol-contract-relative-state-complexity-v1.md').read_bytes()).hexdigest();r['source_sha256']=hashlib.sha256((ROOT/'experiment/src/pnp_architecture/contract_complexity_v1.py').read_bytes()).hexdigest()
 a.output.parent.mkdir(parents=True,exist_ok=True);a.summary.parent.mkdir(parents=True,exist_ok=True);a.output.open('x').write(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
 lines=['# Contract-relative state complexity v1','','| Architecture | Retained bytes | Observation | Update | Decision | Evidence |','|---|---:|---:|---:|---:|---:|']
 for n,c in r['costs'].items():lines.append('| %s | %d | %d | %d | %d | %d |'%(n,c['retained_state_bytes'],c['observation_cost_per_event'],c['update_cost_per_event'],c['decision_cost_per_query'],c['evidence_cost_per_update']))
 text='\n'.join(lines)+f"\n\nK_G={r['K_G']}; I_G={r['I_G_bits']} ideal fixed-length bits; reachable histories={r['history_count']}; bounded partition factorization={r['same_state_bounded_factorization']}.\n";a.summary.open('x').write(text);print(text)
if __name__=='__main__':main()
