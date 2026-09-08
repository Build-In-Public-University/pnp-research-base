#!/usr/bin/env python3
"""Rebuild parent session records from live session DB, refresh manifest + sha256 anchors."""
import base64, hashlib, json, os, re, sqlite3
from collections import Counter
from pathlib import Path
import sqlite3
ROOT=Path('/Users/leoguinan/pnp-session-review').resolve()
home=Path.home()
sid=os.environ.get('HERMES_SESSION_ID')

sysp=Path('/Users/leoguinan/hermes-agent').resolve()
import sys
sys.path.insert(0, str(sysp))
sys.path.insert(0, str(ROOT/'scripts'))

from agent.redact import redact_sensitive_text
from archive_tools import sanitize

DB=home/'.hermes/state.db'
db=sqlite3.connect('file:'+str(DB)+'?mode=ro',uri=True)
db.row_factory=sqlite3.Row

cols=[c[1] for c in db.execute('pragma table_info(messages)').fetchall()]
print('columns',cols)

rows=db.execute('select * from messages where session_id=? order by id',(sid,)).fetchall()
print('total rows',len(rows))

def scrub(text):
    if not isinstance(text,str):return text
    text=redact_sensitive_text(text,force=True)
    text=re.sub(r'\b[A-Za-z0-9_-]{2,}(?:\*{3,}|\.{3}|…)[A-Za-z0-9_-]{2,}','[REDACTED MASKED VALUE]',text)
    return sanitize(text)

def transport_norm(text):
    if not isinstance(text,str):return text
    def norm_id(m):return 'transport-'+hashlib.sha256(m[0].encode()).hexdigest()[:16]
    text=re.sub(r'\b(?:call_|fc_)[A-Za-z0-9_-]{16,}',norm_id,text)
    def decode(m):
        v=m[0];pad='='*(-len(v)%4)
        try:p=base64.b64decode(v+pad,validate=True).decode('utf-8')
        except Exception:return v
        if not p or sum(c.isprintable() or c.isspace() for c in p)/len(p)<0.95:return v
        return '[DECODED TRANSPORT TEXT: '+sanitize(p)+']'
    return re.sub(r'(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{80,}={0,2}(?![A-Za-z0-9+/])',decode,text)

out=[]
th=0;seen=set()
for r in rows:
    rec=dict(r)
    rec['transport_normalized']=True
    role=rec['role'];tn=rec['tool_name']
    if role=='tool':
        if tn in ('skill_view','skills_list'):
            rec['content']='[OPERATIONAL SKILL BODY OMITTED: may contain unrelated private-project information; invocation retained]'
        else:
            c=scrub(rec['content'] or '');c=transport_norm(c);rec['content']=c
            if 'transport-' in c:th+=1
    elif role in ('user','assistant'):
        rec['content']=scrub(rec['content'] or '')
    if rec['id'] in seen:continue
    seen.add(rec['id']);out.append(rec)

jsonl='\n'.join(json.dumps(x,ensure_ascii=False,separators=(',',':')) for x in out)+'\n'
rp=ROOT/'conversation'/'records.jsonl';rp.write_text(jsonl,encoding='utf-8')

dialogue=[f'## Record {r["id"]} — {r["role"]}\n\n{r["content"]}\n\n' for r in out if r['role'] in ('user','assistant')]
dp=ROOT/'conversation'/'dialogue.md';dp.write_text(''.join(dialogue),encoding='utf-8')

manifest=Path(ROOT/'manifest.json').read_text()
m=json.loads(manifest)
m['sessions'][0]['records']=len(out)
m['sessions'][0]['active_roles']=dict(Counter(r['role'] for r in out))
m['sessions'][0]['record_files']=((str(rp),str(hashlib.sha256(rp.read_bytes()).hexdigest())),(str(dp),str(hashlib.sha256(dp.read_bytes()).hexdigest())))
m['sessions'][0]['transport_normalized']=True
m['sessions'][0]['normalized_transport_hits']=th
m['sessions'][0]['records_sha256']=str(hashlib.sha256(rp.read_bytes()).hexdigest())
m['sessions'][0]['dialogue_sha256']=str(hashlib.sha256(dp.read_bytes()).hexdigest())
(Path(ROOT/'manifest.json')).write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')

(rp.parent/'records.sha256').write_text(hashlib.sha256(rp.read_bytes()).hexdigest()+'\n')
(dp.parent/'dialogue.sha256').write_text(hashlib.sha256(dp.read_bytes()).hexdigest()+'\n')
(Path(ROOT/'manifest.json').with_suffix('.sha256')).write_text(hashlib.sha256(Path(ROOT/'manifest.json').read_bytes()).hexdigest()+'\n')

print('records bytes',rp.stat().st_size,'dialogue records',len(dialogue),'transport hits',th)
print('records sha',hashlib.sha256(rp.read_bytes()).hexdigest())
print('dialogue sha',hashlib.sha256(dp.read_bytes()).hexdigest())
print('manifest sha',hashlib.sha256(Path(ROOT/'manifest.json').read_bytes()).hexdigest())
print('role counts',dict(Counter(r['role'] for r in out)))
