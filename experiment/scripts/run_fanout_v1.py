import argparse, hashlib, json
from pathlib import Path
from pnp_architecture.fanout_v1 import experiment
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser(); p.add_argument('--output',type=Path,required=True); p.add_argument('--summary',type=Path,required=True); a=p.parse_args()
 if a.output.exists() or a.summary.exists() or a.output.resolve()==a.summary.resolve(): raise SystemExit('output paths must be distinct and new')
 r=experiment(ROOT); r['protocol_sha256']=hashlib.sha256((ROOT/'experiment/docs/protocol-fanout-calibration-v1.md').read_bytes()).hexdigest(); r['source_sha256']=hashlib.sha256((ROOT/'experiment/src/pnp_architecture/fanout_v1.py').read_bytes()).hexdigest()
 a.output.parent.mkdir(parents=True,exist_ok=True); a.summary.parent.mkdir(parents=True,exist_ok=True); a.output.open('x').write(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
 lines=['# Fan-out calibration v1: archive dependency geometry','', '| Fanout | Depth | Affected fraction | Repair nodes | Full-assurance nodes | Exact |','|---:|---:|---:|---:|---:|---|']
 for c in r['cells']: lines.append('| %d | %d | %.3f | %d | %d | %s |' % (c['fanout'],c['depth'],c['affected_fraction'],c['arms']['indexed_incremental']['repair_nodes'],c['arms']['indexed_incremental']['assurance_nodes'],c['arms']['indexed_incremental']['mechanically_exact']))
 lines += ['', 'The archive was copied to temporary storage. Counts are measured local instrument outputs; timing is diagnostic and not universal evidence.']
 a.summary.open('x').write('\n'.join(lines)+'\n'); print('\n'.join(lines))
if __name__=='__main__': main()
