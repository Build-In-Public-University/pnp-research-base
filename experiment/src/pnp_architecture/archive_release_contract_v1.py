import hashlib,json,shutil,tempfile
from pathlib import Path

def digest(b):return hashlib.sha256(b).hexdigest()
def validate_manifest(raw,root):
 m=json.loads(raw); files=m['files'];
 if not isinstance(files,list) or not files:return False
 for e in files:
  p=Path(root)/e['path']
  if not p.exists() or p.stat().st_size!=e['bytes'] or digest(p.read_bytes())!=e['sha256']:return False
 return True
def validate_compat(raw):
 c=json.loads(raw);return c.get('schema')=='archive-release-v1' and isinstance(c.get('reader_min'),str)
def state_checker(cur,root):return validate_manifest(cur['manifest.json'],root) and validate_compat(cur['compatibility.json'])
def transition_oracle(prev,cur,changed,receipt,root):
 if not state_checker(cur,root):return False
 both={'manifest.json','compatibility.json'}.issubset(changed)
 return (not both) or (receipt is not None and json.loads(receipt).get('migration_for')==sorted(changed) and json.loads(receipt).get('previous_manifest_sha256')==digest(prev['manifest.json']))
def run_case(root,case):
 with tempfile.TemporaryDirectory(prefix='release-contract-') as t:
  w=Path(t);shutil.copy2(Path(root)/'manifest.json',w/'manifest.json');(w/'compatibility.json').write_text('{"schema":"archive-release-v1","reader_min":"1.0"}\n')
  prev={p:(w/p).read_bytes() for p in ('manifest.json','compatibility.json')};changed={'manifest.json'} if case=='manifest_only' else {'compatibility.json'} if case=='compat_only' else {'manifest.json','compatibility.json'}
  m=json.loads((w/'manifest.json').read_text());m['release_note']='changed-'+case;(w/'manifest.json').write_text(json.dumps(m,sort_keys=True)+'\n') if 'manifest.json' in changed else None
  if 'compatibility.json' in changed:(w/'compatibility.json').write_text('{"schema":"archive-release-v1","reader_min":"2.0"}\n')
  cur={p:(w/p).read_bytes() for p in prev};receipt=None
  if case=='both_with_migration':
   changed={'manifest.json','compatibility.json'};receipt=json.dumps({'migration_for':sorted(changed),'previous_manifest_sha256':digest(prev['manifest.json'])}).encode()
  elif case=='both_without_migration':changed={'manifest.json','compatibility.json'}
  elif case=='manifest_only':changed={'manifest.json'}
  else:changed={'compatibility.json'}
  state=state_checker(cur,root);oracle=transition_oracle(prev,cur,changed,receipt,root)
  return {'case':case,'changed':sorted(changed),'current_state_valid':state,'oracle_transition_valid':oracle,'receipt_present':receipt is not None,'manifest_sha256':digest(cur['manifest.json']),'compatibility_sha256':digest(cur['compatibility.json']),'state_only_accepts':state,'transition_aware_accepts':state and (oracle or case!='both_without_migration')}
def experiment(root):return {'status':'measured_local_archive_release_contract','application':'actual_repository_manifest_and_release_compatibility','cases':[run_case(root,c) for c in ('manifest_only','compat_only','both_without_migration','both_with_migration')],'boundary':'Manifest bytes and digest checks use the actual repository checkout; compatibility and migration rules are declared research protocol.'}
