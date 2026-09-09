import argparse,json,hashlib
from pathlib import Path
from pnp_architecture.physical_architecture_benchmark_v1 import benchmark
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path,required=True);a=p.parse_args()
 r=benchmark();r['protocol_sha256']=hashlib.sha256((ROOT/'experiment/docs/protocol-physical-architecture-benchmark-v1.md').read_bytes()).hexdigest();r['source_sha256']=hashlib.sha256((ROOT/'experiment/src/pnp_architecture/physical_architecture_benchmark_v1.py').read_bytes()).hexdigest();a.output.open('x').write(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
 lines=['# Physical architecture benchmark v1','','Local calibration; modeled logical I/O, actual local timing.','','| n | ratio | architecture | exact | wall ns | CPU ns | peak alloc | read B | write B |','|---:|---:|---|---|---:|---:|---:|---:|---:|']
 for x in r['rows']:lines.append('| %d | %s | %s | %s | %d | %d | %d | %d | %d |'%(x['n'],x['query_update_ratio'],x['architecture'],x['exact'],x['wall_ns_median'],x['cpu_ns_median'],x['tracemalloc_peak_bytes_median'],x['logical_read_bytes'],x['logical_write_bytes']))
 a.summary.open('x').write('\n'.join(lines)+'\n\nNo energy counter was used; tracemalloc and logical I/O are proxies.\n');print(a.summary.read_text())
if __name__=='__main__':main()
