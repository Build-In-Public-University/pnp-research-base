import argparse,hashlib,json
from pathlib import Path
from pnp_architecture.interaction_v1 import experiment
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path,required=True);a=p.parse_args()
 if a.output.exists() or a.summary.exists() or a.output.resolve()==a.summary.resolve():raise SystemExit('output paths must be new and distinct')
 r=experiment(ROOT);r['protocol_sha256']=hashlib.sha256((ROOT/'experiment/docs/protocol-semantic-interaction-v1.md').read_bytes()).hexdigest();r['source_sha256']=hashlib.sha256((ROOT/'experiment/src/pnp_architecture/interaction_v1.py').read_bytes()).hexdigest()
 a.output.parent.mkdir(parents=True,exist_ok=True);a.summary.parent.mkdir(parents=True,exist_ok=True);a.output.open('x').write(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
 lines=['# Semantic interaction calibration v1','','| Case | Join | Union | Joint | Interaction | Union exact | Aware exact |','|---|---:|---:|---:|---:|---|---|']
 for c in r['cells']:lines.append('| %s | %d | %d | %d | %d | %s | %s |'%(c['case'],c['join_width'],c['union_nodes'],c['joint_nodes'],c['interaction_nodes'],c['arms']['union_repair']['mechanically_exact'],c['arms']['interaction_aware_repair']['mechanically_exact']))
 text='\n'.join(lines)+'\n\nJoint constraints are explicit fixture rules, not inferred semantic evidence. Timing is diagnostic local data.\n';a.summary.open('x').write(text);print(text)
if __name__=='__main__':main()
