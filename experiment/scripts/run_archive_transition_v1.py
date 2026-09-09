import argparse,hashlib,json
from pathlib import Path
from pnp_architecture.archive_transition_v1 import experiment
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path,required=True);a=p.parse_args()
 if a.output.exists() or a.summary.exists() or a.output.resolve()==a.summary.resolve():raise SystemExit('output paths must be new and distinct')
 r=experiment(ROOT);r['protocol_sha256']=hashlib.sha256((ROOT/'experiment/docs/protocol-archive-transition-interaction-v1.md').read_bytes()).hexdigest();r['source_sha256']=hashlib.sha256((ROOT/'experiment/src/pnp_architecture/archive_transition_v1.py').read_bytes()).hexdigest()
 a.output.parent.mkdir(parents=True,exist_ok=True);a.summary.parent.mkdir(parents=True,exist_ok=True);a.output.open('x').write(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
 lines=['# Archive transition interaction calibration v1','','| Case | Singleton exact | State exact | Transition exact | Oracle artifacts |','|---|---|---|---|---|']
 for c in r['cases']:
  a1=c['arms'];lines.append('| %s | %s | %s | %s | %s |'%(c['case'],a1['singleton_only']['mechanically_exact'],a1['state_complete']['mechanically_exact'],a1['transition_aware']['mechanically_exact'],','.join(c['oracle_artifacts'])))
 text='\n'.join(lines)+'\n\nThe transition rule is explicit and application-specific; it is not inferred semantic evidence.\n';a.summary.open('x').write(text);print(text)
if __name__=='__main__':main()
