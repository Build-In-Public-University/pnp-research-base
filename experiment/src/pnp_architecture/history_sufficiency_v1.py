import hashlib,json,tempfile
from pathlib import Path

def sha(b):return hashlib.sha256(b).hexdigest()
def witness(root):
 current=Path(root).joinpath('manifest.json').read_bytes(); compat=b'{"schema":"archive-release-v1","reader_min":"2.0"}\n'; prev=sha(Path(root).joinpath('manifest.json').read_bytes())
 base={'previous_manifest_sha256':prev,'changed':['compatibility.json','manifest.json'],'current_manifest_sha256':sha(current),'current_compatibility_sha256':sha(compat)}
 valid=dict(base, migration_present=True, migration_sha256=sha(json.dumps(base,sort_keys=True).encode()))
 invalid=dict(base,migration_present=False,migration_sha256=None)
 histories=[('missing',invalid,False),('satisfied',valid,True)]
 def rep(name,h):
  if name=='current_only':return {'manifest':h['current_manifest_sha256'],'compatibility':h['current_compatibility_sha256']}
  if name=='event_log':return {'events':[{'kind':'release','changed':h['changed']},{'migration_present':h['migration_present'],'previous':h['previous_manifest_sha256']}]}
  if name=='transition_record':return {k:h[k] for k in ('previous_manifest_sha256','changed','migration_present','migration_sha256')}
  if name=='digest_summary':return sha(json.dumps(rep('transition_record',h),sort_keys=True).encode())
  if name=='minimal_state':return 'migration_satisfied' if h['migration_present'] else 'migration_missing'
 reps={}
 for name in ('current_only','event_log','transition_record','digest_summary','minimal_state'):
  rows=[]
  for label,h,outcome in histories:
   r=rep(name,h); raw=json.dumps(r,sort_keys=True,separators=(',',':')).encode() if not isinstance(r,str) else r.encode()
   rows.append({'history':label,'representation':r,'representation_bytes':len(raw),'maintenance_bytes':len(raw),'query_bytes':len(raw),'oracle_outcome':outcome})
  equal=rows[0]['representation']==rows[1]['representation']; reps[name]={'rows':rows,'indistinguishable':equal,'exact_for_pair':not equal}
 return {'theorem':'If R(h1)=R(h2) and G(h1)!=G(h2), no exact checker over R exists for both histories.','contract':'both manifest and compatibility change requires migration evidence bound to previous manifest','representations':reps}
def experiment(root):return witness(root)
