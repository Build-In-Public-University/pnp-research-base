import argparse,hashlib,json
from pathlib import Path
from pnp_architecture.history_sufficiency_v1 import experiment
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path,required=True);a=p.parse_args()
 if a.output.exists() or a.summary.exists() or a.output.resolve()==a.summary.resolve():raise SystemExit('output paths must be new and distinct')
 r=experiment(ROOT);r['protocol_sha256']=hashlib.sha256((ROOT/'experiment/docs/protocol-history-sufficiency-v1.md').read_bytes()).hexdigest();r['source_sha256']=hashlib.sha256((ROOT/'experiment/src/pnp_architecture/history_sufficiency_v1.py').read_bytes()).hexdigest()
 a.output.parent.mkdir(parents=True,exist_ok=True);a.summary.parent.mkdir(parents=True,exist_ok=True);a.output.open('x').write(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
 lines=['# History sufficiency calibration v1','','| Representation | Same for witness pair | Exact pair distinction | Missing-case bytes | Satisfied-case bytes |','|---|---|---|---:|---:|']
 for n,x in r['representations'].items():lines.append('| %s | %s | %s | %d | %d |'%(n,x['indistinguishable'],x['exact_for_pair'],x['rows'][0]['representation_bytes'],x['rows'][1]['representation_bytes']))
 text='\n'.join(lines)+'\n\nThe current-state representation is the deliberate impossibility witness; retained representations are trusted controls.\n';a.summary.open('x').write(text);print(text)
if __name__=='__main__':main()
