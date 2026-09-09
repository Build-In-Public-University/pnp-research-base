import hashlib,json,shutil,tempfile
from pathlib import Path
CASES={'manifest_only':('manifest.json',),'compat_only':('compatibility.json',),'both':('manifest.json','compatibility.json')}
ART=('manifest-check','compatibility-check','provenance','migration-approval')
def h(*parts):
 x=hashlib.sha256()
 for p in parts:x.update(p)
 return x.digest()
def run_case(root,case):
 with tempfile.TemporaryDirectory(prefix='archive-transition-') as t:
  w=Path(t); m=Path(root)/'manifest.json'; shutil.copy2(m,w/'manifest.json'); (w/'compatibility.json').write_text('{"schema":"archive-v1","manifest":"manifest.json"}\n')
  old={p:(w/p).read_bytes() for p in ('manifest.json','compatibility.json')};changed=set(CASES[case])
  for p in changed:
   with (w/p).open('ab') as f:f.write(('\nrelease-change-'+p).encode())
  new={p:(w/p).read_bytes() for p in old};
  def state_values(inp,transition=False):
   vals={'manifest-check':h(inp['manifest.json'],b'manifest-check'),'compatibility-check':h(inp['compatibility.json'],b'compatibility-check'),'provenance':h(inp['manifest.json'],inp['compatibility.json'],b'provenance')}
   if transition: vals['migration-approval']=h(old['manifest.json'],old['compatibility.json'],inp['manifest.json'],inp['compatibility.json'],b'migration-approval')
   return vals
  expected=state_values(new,len(changed)==2);before=state_values(old); singleton={'manifest-check','compatibility-check'}
  if case in ('manifest_only','both'): singleton={'manifest-check','provenance'} if case=='manifest_only' else {'manifest-check','compatibility-check','provenance'}
  if case=='compat_only':singleton={'compatibility-check','provenance'}
  state={'manifest-check','compatibility-check','provenance'}; transition=set(state)|({'migration-approval'} if case=='both' else set())
  policies={'singleton_only':singleton,'state_complete':state,'transition_aware':transition};arms={}
  for name,selected in policies.items():
   vals=dict(before)
   for a in selected:
    if a=='manifest-check':vals[a]=h(new['manifest.json'],b'manifest-check')
    elif a=='compatibility-check':vals[a]=h(new['compatibility.json'],b'compatibility-check')
    elif a=='provenance':vals[a]=h(new['manifest.json'],new['compatibility.json'],b'provenance')
    else:vals[a]=h(old['manifest.json'],old['compatibility.json'],new['manifest.json'],new['compatibility.json'],b'migration-approval')
   arms[name]={'repair_artifacts':sorted(selected),'repair_count':len(selected),'mechanically_exact':vals==expected}
  return {'case':case,'changed_inputs':sorted(changed),'oracle_artifacts':sorted(expected),'arms':arms}
def experiment(root):return {'status':'measured_local_archive_transition_interaction','application':'archive_release_manifest_compatibility','cases':[run_case(root,c) for c in CASES],'boundary':'Temporary release fixture with explicit state and transition contracts.'}
