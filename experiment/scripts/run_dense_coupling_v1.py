import argparse,hashlib,json
from pathlib import Path
from pnp_architecture.dense_coupling_v1 import experiment
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path,required=True);a=p.parse_args()
 if a.output.exists() or a.summary.exists() or a.output.resolve()==a.summary.resolve():raise SystemExit('output paths must be distinct and new')
 r=experiment(ROOT);r['protocol_sha256']=hashlib.sha256((ROOT/'experiment/docs/protocol-dense-coupling-v1.md').read_bytes()).hexdigest();r['source_sha256']=hashlib.sha256((ROOT/'experiment/src/pnp_architecture/dense_coupling_v1.py').read_bytes()).hexdigest()
 a.output.parent.mkdir(parents=True,exist_ok=True);a.summary.parent.mkdir(parents=True,exist_ok=True);a.output.open('x').write(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
 lines=['# Dense-coupling calibration v1','','| Fanout | Join width | rho | Full repair edges | Incremental repair edges | Exact |','|---:|---:|---:|---:|---:|---|']
 for c in r['cells']:lines.append('| %d | %d | %.3f | %d | %d | %s |'%(c['fanout'],c['join_width'],c['affected_nodes']/c['derived_nodes'],c['arms']['full_recompute']['edge_checks'],c['arms']['indexed_incremental']['edge_checks'],c['arms']['indexed_incremental']['mechanically_exact']))
 text='\n'.join(lines)+'\n\nCounts are local instrument outputs over temporary copies; timing is diagnostic, not universal evidence.\n';a.summary.open('x').write(text);print(text)
if __name__=='__main__':main()
