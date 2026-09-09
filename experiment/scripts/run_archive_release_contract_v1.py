import argparse,hashlib,json
from pathlib import Path
from pnp_architecture.archive_release_contract_v1 import experiment
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path,required=True);a=p.parse_args()
 if a.output.exists() or a.summary.exists() or a.output.resolve()==a.summary.resolve():raise SystemExit('output paths must be new and distinct')
 r=experiment(ROOT);r['protocol_sha256']=hashlib.sha256((ROOT/'experiment/docs/protocol-archive-release-contract-v1.md').read_bytes()).hexdigest();r['source_sha256']=hashlib.sha256((ROOT/'experiment/src/pnp_architecture/archive_release_contract_v1.py').read_bytes()).hexdigest()
 a.output.parent.mkdir(parents=True,exist_ok=True);a.summary.parent.mkdir(parents=True,exist_ok=True);a.output.open('x').write(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
 lines=['# Archive release-contract calibration v1','','| Case | Current-state valid | State-only accepts | Transition oracle |','|---|---|---|---|']
 for c in r['cases']:lines.append('| %s | %s | %s | %s |'%(c['case'],c['current_state_valid'],c['state_only_accepts'],c['oracle_transition_valid']))
 text='\n'.join(lines)+'\n\nManifest validation used the actual repository checkout; compatibility and migration rules are declared protocol contracts.\n';a.summary.open('x').write(text);print(text)
if __name__=='__main__':main()
