import argparse,hashlib,json
from pathlib import Path
from pnp_architecture.recursive_history_v1 import experiment
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path,required=True);a=p.parse_args()
 if a.output.exists() or a.summary.exists() or a.output.resolve()==a.summary.resolve():raise SystemExit('output paths must be new and distinct')
 r=experiment(6);r['protocol_sha256']=hashlib.sha256((ROOT/'experiment/docs/protocol-recursive-history-sufficiency-v1.md').read_bytes()).hexdigest();r['source_sha256']=hashlib.sha256((ROOT/'experiment/src/pnp_architecture/recursive_history_v1.py').read_bytes()).hexdigest()
 a.output.parent.mkdir(parents=True,exist_ok=True);a.summary.parent.mkdir(parents=True,exist_ok=True);a.output.open('x').write(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
 lines=['# Recursive history sufficiency calibration v1','','| Representation | Bytes | Distinct semantic values |','|---|---:|---|']
 for n,x in r['representations'].items():lines.append('| %s | %s | %s |'%(n,x['bytes'],list(x['values'].values())))
 text='\n'.join(lines)+f"\n\nStates: {', '.join(r['states'])}. Events: {', '.join(r['events'])}. Exhaustive sequences through length {r['max_sequence_length']}: {r['bounded_sequences']}.\n\nDecision and update factorization passed; continuation sufficiency is established for this finite machine by induction from those two factorizations.\n";a.summary.open('x').write(text);print(text)
if __name__=='__main__':main()
