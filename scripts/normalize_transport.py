#!/usr/bin/env python3
"""Normalize non-semantic transport IDs; expose text encoding to redaction.

Run after build_archive.py and before verification. Mutates this local draft only.
"""
import base64
import hashlib
import json
from pathlib import Path
import re
from archive_tools import sanitize

ROOT=Path(__file__).resolve().parents[1]

def norm(text):
    text=re.sub(r'\b(?:call_|fc_)[A-Za-z0-9_-]{16,}',lambda m:'transport-'+hashlib.sha256(m[0].encode()).hexdigest()[:16],text)
    def decoded(m):
        value=m[0]
        try:
            plain=base64.b64decode(value+'='*(-len(value)%4),validate=True).decode('utf-8')
            if not plain or sum(c.isprintable() or c.isspace() for c in plain)/len(plain)<0.95:return value
        except (ValueError,UnicodeError):return value
        return '[DECODED TRANSPORT TEXT: '+sanitize(plain)+']'
    return re.sub(r'(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{80,}={0,2}(?![A-Za-z0-9+/])',decoded,text)

def recurse(x):
    if isinstance(x,str):return norm(x)
    if isinstance(x,list):return [recurse(v) for v in x]
    if isinstance(x,dict):return {k:recurse(v) for k,v in x.items()}
    return x

def main():
    m=json.loads((ROOT/'manifest.json').read_text())
    renamed={}
    for i,s in enumerate(m['sessions'][1:],1):
        old='conversation/subagents/'+s['session_id'];new=f'conversation/subagents/worker-{i}'
        p=ROOT/old
        if p.exists():p.rename(ROOT/new)
        renamed[old]=new
    for e in m['files']:
        old=e['path'];new=old
        for a,b in renamed.items():new=new.replace(a,b)
        if new.startswith('sources/reviews/subagent-summary-'):
            new='sources/reviews/review-'+str(len([v for v in renamed if v.startswith('sources/reviews/')])+1)+'.txt'
            (ROOT/old).rename(ROOT/new);renamed[old]=new
        e['path']=new
        p=ROOT/new;data=p.read_bytes()
        if new.startswith('conversation/'):
            if p.suffix=='.jsonl':
                data=(''.join(json.dumps(recurse(json.loads(line)),ensure_ascii=False)+'\n' for line in p.read_text().splitlines())).encode()
            else:data=norm(p.read_text()).encode()
            p.write_bytes(data)
        e['sha256']=hashlib.sha256(data).hexdigest();e['bytes']=len(data)
    m['transport_normalization']='Opaque call/response IDs mapped deterministically to transport-hex labels. UTF-8 base64 payloads decoded and scrubbed inline; tool command syntax may no longer be executable. Subagent and review file paths shortened. Record IDs unchanged.'
    (ROOT/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
