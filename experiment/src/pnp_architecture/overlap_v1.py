import hashlib,json,shutil,tempfile,time
from pathlib import Path
SETS={'single':(0,),'disjoint':(0,6),'adjacent':(0,1),'cluster':(0,1,2,3)}
def _hash(parts):
 h=hashlib.sha256()
 for p in parts:h.update(p)
 return h.digest()
def graph(n=12,j=1): return [tuple((i+k)%n for k in range(j)) for i in range(n)]
def run_cell(root,pattern,j,assurance='full'):
 es=json.loads((Path(root)/'manifest.json').read_text())['files'][:12];g=graph(12,j)
 with tempfile.TemporaryDirectory(prefix='overlap-') as tmp:
  w=Path(tmp)
  for e in es:
   p=w/e['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(Path(root)/e['path'],p)
  old={e['path']:(w/e['path']).read_bytes() for e in es}
  def calc(inp,which=None):
   out=[];edges=0
   for i,deps in enumerate(g):
    if which is not None and i not in which:out.append(None);continue
    out.append(_hash([inp[es[d]['path']] for d in deps]));edges+=len(deps)
   return out,edges
  before,_=calc(old)
  changed=SETS[pattern]
  for i in changed:
   with (w/es[i]['path']).open('ab') as f:f.write(b'\noverlap-update-'+str(i).encode())
  new={e['path']:(w/e['path']).read_bytes() for e in es};oracle,_=calc(new)
  sets=[{i for i,deps in enumerate(g) if base in deps} for base in changed]
  union=set().union(*sets); isolated=sum(map(len,sets)); total=len(g)
  arms={}
  for name,which in [('full_recompute',set(range(total))),('indexed_incremental',union)]:
   _,repair_ns=_t(lambda:calc(new,which));_,edges=calc(new,which)
   assure=set(range(total)) if assurance=='full' else which;_,assure_ns=_t(lambda:calc(new,assure))
   vals=list(before)
   for i in which: vals[i]=_hash([new[es[d]['path']] for d in g[i]])
   arms[name]={'repair_nodes':len(which),'edge_checks':edges,'assurance_nodes':len(assure),'repair_ns':repair_ns,'assurance_ns':assure_ns,'mechanically_exact':vals==oracle if name!='full_recompute' else True,'transport_bytes':len(json.dumps({'pattern':pattern,'j':j}).encode())}
  return {'pattern':pattern,'join_width':j,'changed_inputs':len(changed),'index_edges':total*j,'isolated_affected_sum':isolated,'union_affected_nodes':len(union),'overlap_savings':isolated-len(union),'assurance_scope':assurance,'arms':arms}
def _t(fn):
 s=time.perf_counter_ns();v=fn();return v,time.perf_counter_ns()-s
def experiment(root):return {'status':'measured_local_overlapping_updates','application':'archive_manifest_dependency_geometry','cells':[run_cell(root,p,j,a) for p in SETS for j in (1,2,4) for a in ('full','affected')],'boundary':'Local temporary-file measurement; timing diagnostic only.'}
