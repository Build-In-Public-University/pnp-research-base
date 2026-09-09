import argparse,hashlib,json
from pathlib import Path
from pnp_architecture.fixed_contract_architecture_v1 import experiment
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path,required=True);a=p.parse_args()
 if a.output.exists() or a.summary.exists() or a.output.resolve()==a.summary.resolve():raise SystemExit('output paths must be new and distinct')
 r=experiment(range(1,9));r['protocol_sha256']=hashlib.sha256((ROOT/'experiment/docs/protocol-fixed-contract-architecture-v1.md').read_bytes()).hexdigest();r['source_sha256']=hashlib.sha256((ROOT/'experiment/src/pnp_architecture/fixed_contract_architecture_v1.py').read_bytes()).hexdigest()
 a.output.parent.mkdir(parents=True,exist_ok=True);a.summary.parent.mkdir(parents=True,exist_ok=True);a.output.open('x').write(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
 lines=['# Fixed-contract architecture v1','','| n | Architecture | Exact | Retained bits | Update | Decision | Evidence |','|---:|---|---|---:|---:|---:|---:|']
 for x in r['rows']:lines.append('| %d | %s | %s | %d | %d | %d | %d |'%(x['n'],x['architecture'],x['exact'],x['retained_bits'],x['update_work'],x['decision_work'],x['evidence_work']))
 text='\n'.join(lines)+'\n\nAll architectures implement the same fixed contract; costs are modeled units, not timings.\n';a.summary.open('x').write(text);print(text)
if __name__=='__main__':main()
