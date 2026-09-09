import hashlib,json,shutil,tempfile,time
from pathlib import Path
CASES={'disjoint':((0,),(6,)),'adjacent':((0,),(1,)),'joint':((0,1),),'cluster':((0,1),(2,3))}
def _h(parts):
 h=hashlib.sha256()
 for p in parts:h.update(p)
 return h.digest()
def run_cell(root,case,join_width):
 es=json.loads((Path(root)/'manifest.json').read_text())['files'][:12];groups=CASES[case]
 deps=[tuple((i+k)%12 for k in range(join_width)) for i in range(12)]
 with tempfile.TemporaryDirectory(prefix='interaction-') as t:
  w=Path(t)
  for e in es:
   p=w/e['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(Path(root)/e['path'],p)
  old={e['path']:(w/e['path']).read_bytes() for e in es}
  joint_active=False
  def calc(inp,which=None,interaction=False):
   out=[];edges=0
   for i,ds in enumerate(deps):
    if which is not None and i not in which:out.append(None);continue
    parts=[inp[es[d]['path']] for d in ds]
    if interaction and i==8: parts.append(b'joint-constraint')
    out.append(_h(parts));edges+=len(ds)
   return out,edges
  before,_=calc(old)
  changed=set().union(*groups)
  for i in changed:
   with (w/es[i]['path']).open('ab') as f:f.write(b'\ninteraction-'+str(i).encode())
  new={e['path']:(w/e['path']).read_bytes() for e in es};joint_active=case in ('joint','cluster')
  oracle,_=calc(new,interaction=joint_active)
  individual=[{i for i,ds in enumerate(deps) if base in ds} for group in groups for base in group]
  union=set().union(*individual) if individual else set();
  joint=set(union)
  if case in ('joint','cluster'): joint.add(8)
  interaction=len(joint-union);full=set(range(12))
  arms={}
  for name,which in [('union_repair',union),('interaction_aware_repair',joint),('full_recompute',full)]:
   s=time.perf_counter_ns();vals=list(before)
   for i in which:
    parts=[new[es[d]['path']] for d in deps[i]]
    if joint_active and i==8: parts.append(b'joint-constraint')
    vals[i]=_h(parts)
   elapsed=time.perf_counter_ns()-s;arms[name]={'repair_nodes':len(which),'edge_checks':len(which)*join_width,'repair_ns':elapsed,'mechanically_exact':vals==oracle}
  return {'case':case,'join_width':join_width,'changed_inputs':len(changed),'union_nodes':len(union),'joint_nodes':len(joint),'interaction_nodes':interaction,'interaction_fraction':interaction/12,'index_edges':12*join_width,'arms':arms}
def experiment(root):return {'status':'measured_local_semantic_interaction','application':'archive_manifest_dependency_geometry','cells':[run_cell(root,c,j) for c in CASES for j in (1,2,4)],'boundary':'Synthetic joint-constraint fixture over temporary archive copies; interaction rule is explicit and not inferred from semantic data.'}
