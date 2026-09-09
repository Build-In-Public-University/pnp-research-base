import hashlib,json,shutil,tempfile,time
from pathlib import Path

def _hash(parts):
 h=hashlib.sha256()
 for p in parts:h.update(p)
 return h.digest()
def _t(fn):
 s=time.perf_counter_ns();v=fn();return v,time.perf_counter_ns()-s

def graph(base_count=12,fanout=1,join_width=1):
 if not 1<=fanout<base_count or not 1<=join_width<=base_count:raise ValueError('invalid geometry')
 out=[]
 for i in range(base_count):
  if i<fanout: deps=[0]
  else: deps=[max(1,(i+1)%base_count)]
  for k in range(1,join_width): deps.append((i+k+1)%base_count or 1)
  out.append(tuple(deps))
 return out

def run_join_cell(root,fanout,join_width,assurance='full'):
 root=Path(root);entries=json.loads((root/'manifest.json').read_text())['files'][:12]
 with tempfile.TemporaryDirectory(prefix='dense-join-') as tmp:
  work=Path(tmp)
  for e in entries:
   p=work/e['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/e['path'],p)
  g=graph(12,fanout,join_width); old={e['path']:(work/e['path']).read_bytes() for e in entries}
  def calc(inputs,selected=None):
   vals=[];checks=0
   for i,deps in enumerate(g):
    if selected is not None and i not in selected: vals.append(None);continue
    vals.append(_hash([inputs[entries[d]['path']] for d in deps]));checks+=len(deps)
   return vals,checks
  before,_=calc(old)
  with (work/entries[0]['path']).open('ab') as f:f.write(b'\njoin-update')
  new={e['path']:(work/e['path']).read_bytes() for e in entries};oracle,_=calc(new)
  total=len(g);affected=set(range(fanout));result={}
  for arm in ('full_recompute','indexed_incremental'):
   selected=set(range(total)) if arm=='full_recompute' else affected
   _,repair_ns=_t(lambda:calc(new,selected))
   _,checks=calc(new,selected)
   assurance_set=set(range(total)) if assurance=='full' else selected
   _,assure_ns=_t(lambda:calc(new,assurance_set))
   vals=list(before)
   for i in selected:
    vals[i]=_hash([new[entries[d]['path']] for d in g[i]])
   exact=vals==oracle if arm=='indexed_incremental' else True
   result[arm]={'repair_nodes':len(selected),'edge_checks':checks,'assurance_nodes':len(assurance_set),'repair_ns':repair_ns,'assurance_ns':assure_ns,'mechanically_exact':exact,'transport_bytes':len(json.dumps({'f':fanout,'j':join_width}).encode())}
  return {'fanout':fanout,'join_width':join_width,'derived_nodes':total,'index_edges':total*join_width,'affected_nodes':fanout,'affected_edge_checks':fanout*join_width,'assurance_scope':assurance,'arms':result}

def experiment(root):
 return {'status':'measured_local_dense_coupling','application':'archive_manifest_dependency_geometry','cells':[run_join_cell(root,f,j,a) for f in (1,2,4,8,11) for j in (1,2,4) for a in ('full','affected')],'boundary':'Local temporary-file measurement; timing diagnostic only.'}
