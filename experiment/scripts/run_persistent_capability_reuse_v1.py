import argparse,json,hashlib
from pathlib import Path
from pnp_architecture.persistent_capability_reuse_v1 import experiment
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path,required=True);a=p.parse_args();r=experiment();r['protocol_sha256']=hashlib.sha256((ROOT/'experiment/docs/protocol-persistent-capability-reuse-v1.md').read_bytes()).hexdigest();r['source_sha256']=hashlib.sha256((ROOT/'experiment/src/pnp_architecture/persistent_capability_reuse_v1.py').read_bytes()).hexdigest();a.output.open('x').write(json.dumps(r,sort_keys=True,indent=2)+'\n');text='# Persistent capability reuse v1\n\n| n | Fresh | Persistent remote | Local replica | Best |\n|---:|---:|---:|---:|---|\n'+''.join(f"| {x['n']} | {x['totals']['fresh']} | {x['totals']['persistent_remote']} | {x['totals']['local_replica']} | {x['best']} |\n" for x in r['rows']);a.summary.open('x').write(text);print(text)
if __name__=='__main__':main()
