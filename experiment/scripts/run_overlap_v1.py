import argparse,hashlib,json
from pathlib import Path
from pnp_architecture.overlap_v1 import experiment
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path,required=True);a=p.parse_args()
 if a.output.exists() or a.summary.exists() or a.output.resolve()==a.summary.resolve():raise SystemExit('output paths must be new and distinct')
 r=experiment(ROOT);r['protocol_sha256']=hashlib.sha256((ROOT/'experiment/docs/protocol-overlapping-updates-v1.md').read_bytes()).hexdigest();r['source_sha256']=hashlib.sha256((ROOT/'experiment/src/pnp_architecture/overlap_v1.py').read_bytes()).hexdigest()
 a.output.parent.mkdir(parents=True,exist_ok=True);a.summary.parent.mkdir(parents=True,exist_ok=True);a.output.open('x').write(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
 lines=['# Overlapping updates calibration v1','','| Pattern | Join width | Isolated sum | Union | Overlap savings | Exact |','|---|---:|---:|---:|---:|---|']
 for c in r['cells']:lines.append('| %s | %d | %d | %d | %d | %s |'%(c['pattern'],c['join_width'],c['isolated_affected_sum'],c['union_affected_nodes'],c['overlap_savings'],c['arms']['indexed_incremental']['mechanically_exact']))
 text='\n'.join(lines)+'\n\nCounts are local instrument outputs over temporary copies; timing is diagnostic, not universal evidence.\n';a.summary.open('x').write(text);print(text)
if __name__=='__main__':main()
