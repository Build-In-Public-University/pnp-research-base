#!/usr/bin/env python3
"""Rebuild parent session records from the live session DB for the current Hermes session, refresh the local manifest and sha256 anchors, keep everything else unchanged."""
import base64, hashlib, json, os, re, sqlite3
from pathlib import Path

ROOT=Path('/Users/leoguinan/pnp-session-review').resolve()
home=Path.home()
sid=os.environ.get('HERMES_SESSION_ID')

sys_path=Path('/Users/leoguinan/hermes-agent').resolve()
import sys
sys.path.insert(0, str(sys_path))
sys.path.insert(0, str(ROOT/'scripts'))

from agent.redact import redact_sensitive_text
from archive_tools import sanitize

def scrub_text(text):
    if not isinstance(text,str):
        return text
    text=redact_sensitive_text(text,force=True)
    text=re.sub(r'\b[A-Za-z0-9_-]{2,}(?:\*{3,}|\.{3}|…)[A-Za-z0-9_-]{2,}','[REDACTED MASKED VALUE]',text)
    return sanitize(text)

def transport_normalize(text):
    if not isinstance(text,str):
        return text
    def norm_id(m):
        return 'transport-'+hashlib.sha256(m[0].encode()).hexdigest()[:16]
    text=re.sub(r'\b(?:call_|fc_)[A-Za-z0-9_-]{16,}', norm_id, text)
    def decode_base64(m):
        value=m[0]; pad='='*(-len(value)%4)
        try:
            plain=base64.b64decode(value+pad,validate=True).decode('utf-8')
            if not plain or sum(c.isprintable() or c.isspace() for c in plain)/len(plain)<0.95:
                return value
        except Exception:
            return value
        return '[DECODED TRANSPORT TEXT: '+sanitize(plain)+']'
    return re.sub(r'(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{80,}={0,2}(?![A-Za-z0-9+/])', decode_base64, text)

db=_sqlite3.connect('file:'+str(home/'.hermes/state.db')+'?mode=ro',uri=True)
db.row_factory=_sqlite3.Row

rows=db.execute('select id,session_id,role,content,tool_call_id,tool_calls,tool_name,active,compacted,timestamp from messages where session_id=? order by id',(sid,)).fetchall()

print('RAW COUNT', len(rows))
print('MAX ID', max(r['id'] for r in rows))

out=[]
transport_hits=0
seen=set()
for r in rows:
    rec=dict(r)
    rec['transport_normalized']=True
    kind=rec.get('record_kind')
    if kind=='context_summary':
        rec['content']='[CONTEXT COMPACTION SUMMARY RECORD]'
    elif rec.get('role')=='tool':
        name=rec.get('tool_name')
        if name in ('skill_view','skills_list'):
            rec['content']='[OPERATIONAL SKILL BODY OMITTED: may contain unrelated private-project information; invocation retained]'
        else:
            rec['content']=scrub_text(rec.get('content') or '')
            rec['content']=transport_normalize(rec['content'])
            if 'transport-' in rec['content']:
                transport_hits+=1
    else:
        rec['content']=scrub_text(rec.get('content') or '')
    if rec['id'] in seen:
        continue
    seen.add(rec['id'])
    out.append(rec)

out_jsonl='\n'.join(json.dumps(x,ensure_ascii=False,separators=(',',':')) for x in out)+'\n'
p=ROOT/'conversation'/'records.jsonl'
p.write_text(out_jsonl,encoding='utf-8')

print('WRITTEN BYTES', p.stat().st_size)
print('TRANSPORT HITS', transport_hits)

dialogue=[]
for rec in out:
    if rec.get('role') in ('user','assistant'):
        dialogue.append('## Record {} — {}\n\n{}\n\n'.format(rec['id'],rec['role'],rec.get('content') or ''))
dp=ROOT/'conversation'/'dialogue.md'
dp.write_text(''.join(dialogue),encoding='utf-8')

import collections
role_counts=dict(collections.Counter(rec['role'] for rec in out))
print('RECORDS', len(out), 'DIALOGUE RECORDS', len(dialogue))
print('ROLE COUNTS', role_counts)

manifest_path=ROOT/'manifest.json'
manifest=json.loads(manifest_path.read_text())
manifest['sessions'][0]['records']=len(out)
manifest['sessions'][0]['active_roles']=role_counts
manifest['sessions'][0]['record_files']=(
    ('conversation/records.jsonl',hashlib.sha256(p.read_bytes()).hexdigest()),
    ('conversation/dialogue.md',hashlib.sha256(dp.read_bytes()).hexdigest()),
)
manifest['sessions'][0]['transport_normalized']=True
manifest['sessions'][0]['normalized_transport_hits']=transport_hits
manifest_path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')

(p.parent/'records.sha256').write_text(hashlib.sha256(p.read_bytes()).hexdigest()+'\n')
(dp.parent/'dialogue.sha256').write_text(hashlib.sha256(dp.read_bytes()).hexdigest()+'\n')
(manifest_path.parent/'manifest.sha256').write_text(hashlib.sha256(manifest_path.read_bytes()).hexdigest()+'\n')

print('RECORDS SHA256', hashlib.sha256(p.read_bytes()).hexdigest())
print('DIALOGUE SHA256', hashlib.sha256(dp.read_bytes()).hexdigest())
print('MANIFEST SHA256', hashlib.sha256(manifest_path.read_bytes()).hexdigest())
print('FILES IN MANIFEST', len(manifest['files']))
