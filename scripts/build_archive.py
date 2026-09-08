#!/usr/bin/env python3
"""Build a bounded local review archive from read-only Hermes records.

Requires the local Hermes Python environment for its additional secret redactor.
Never uploads. Excludes system/developer messages and all reasoning fields.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
from archive_tools import sanitize


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--home',type=Path,required=True)
    ap.add_argument('--session',required=True)
    ap.add_argument('--cutoff',type=int,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args(); home=args.home.resolve(); out=args.out.resolve()
    sys.path.insert(0,str(home/'hermes-agent'))
    from agent.redact import redact_sensitive_text
    def clean(s):
        s=redact_sensitive_text(s,force=True)
        # Remove partially masked credential fragments as well as full values.
        s=re.sub(r'\b[A-Za-z0-9_-]{2,}(?:\*{3,}|\.{3}|…)[A-Za-z0-9_-]{2,}', '[REDACTED MASKED VALUE]', s)
        return sanitize(s)
    def scrub(x):
        if isinstance(x,str): return clean(x)
        if isinstance(x,list):return [scrub(v) for v in x]
        if isinstance(x,dict):return {k:scrub(v) for k,v in x.items()}
        return x
    entries=[]
    def put(rel,data,source,kind,original=None):
        p=out/rel;p.parent.mkdir(parents=True,exist_ok=True)
        if isinstance(data,str):data=data.encode()
        if p.exists():raise FileExistsError(p)
        p.write_bytes(data)
        entries.append(dict(path=rel,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),source=source,kind=kind,
                            source_sha256=hashlib.sha256(original).hexdigest() if original is not None else None,
                            transformed=original is not None and data!=original))
    def copy(src,rel,kind):
        raw=src.read_bytes()
        if src.suffix=='.pdf':data=raw
        else:
            text=raw.decode('utf-8')
            if src.suffix=='.json':
                obj=json.loads(text);changed=scrub(obj)
                data=raw if changed==obj else (json.dumps(changed,sort_keys=True,indent=2)+'\n').encode()
            else:data=clean(text).encode()
        put(rel,data,src.name,kind,raw)
    db=sqlite3.connect('file:'+str(home/'.hermes/state.db')+'?mode=ro',uri=True);db.row_factory=sqlite3.Row
    ids=[args.session]
    for sid in ids:
        ids.extend(r[0] for r in db.execute('select id from sessions where parent_session_id=? order by started_at,id',(sid,)) if r[0] not in ids)
    counts=[]; all_rows=[]; document_reads=[]; web_count=0; skill_count=0
    def calls(x):
        if isinstance(x,list):
            for v in x:yield from calls(v)
        if isinstance(x,dict):
            if 'function' in x:yield from calls(x['function'])
            elif 'name' in x and 'arguments' in x:
                a=x['arguments']
                if isinstance(a,str):
                    try:a=json.loads(a)
                    except ValueError:a={}
                yield x['name'],a
            for k,v in x.items():
                if k not in ('function','arguments'):yield from calls(v)
    for sid in ids:
        rows=db.execute('select id,session_id,role,content,tool_call_id,tool_calls,tool_name,timestamp,active,compacted from messages where session_id=? and id<=? order by id',(sid,args.cutoff)).fetchall()
        records=[]; dialogue=[]
        for r in rows:
            r=dict(r)
            if r['role'] not in ('user','assistant','tool'):continue
            rawcontent=r['content'] or ''
            if r['tool_calls']:
                try:r['tool_calls']=json.loads(r['tool_calls'])
                except ValueError:pass
                for name,a in calls(r['tool_calls']):
                    if name.endswith('read_file') and isinstance(a,dict):document_reads.append(a.get('path',''))
            r['record_kind']='context_summary' if rawcontent.startswith('[CONTEXT COMPACTION') else ('delegation_notification' if rawcontent.startswith('[ASYNC DELEGATION') else r['role'])
            if r['role']=='tool' and r['tool_name'] in ('skill_view','skills_list'):
                skill_count+=1
                r['content']='[OPERATIONAL SKILL BODY OMITTED: may contain unrelated private project information; invocation retained.]'
            if r['role']=='tool' and r['tool_name']=='web_extract' and '{' in rawcontent:
                try:
                    payload,_=json.JSONDecoder().raw_decode(rawcontent[rawcontent.index('{'):])
                    for page in payload.get('results',[]):
                        web_count+=1
                        put(f'sources/web/{r["id"]}-{web_count}.json',json.dumps(scrub(page),ensure_ascii=False,indent=2)+'\n',page.get('url','unknown'),'historical_web_extraction')
                except (ValueError,TypeError):pass
            r=scrub(r);records.append(r);all_rows.append(r)
            if r['role'] in ('user','assistant') and r['content']:
                target=dialogue
                if r['record_kind']=='context_summary':continue
                target.append(f'## Record {r["id"]} — {r["role"]}\n\nStored active={r["active"]}; compacted={r["compacted"]}.\n\n{r["content"]}\n')
        prefix='conversation' if sid==args.session else f'conversation/subagents/{sid}'
        put(prefix+'/records.jsonl',''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records),sid,'stored_records_redacted')
        put(prefix+'/dialogue.md','# Stored dialogue\n\nContext summaries are in records.jsonl, not repeated here. Inactive historical rows and replayed text are retained; ordering is database ID order, not deduplicated chronology.\n\n'+'\n'.join(dialogue),sid,'readable_dialogue')
        counts.append(dict(session_id=sid,records=len(records),roles=dict(Counter(r['role'] for r in records)),context_summaries=sum(r['record_kind']=='context_summary' for r in records),compacted=sum(bool(r['compacted']) for r in records)))
    names=['boussinesq.pdf','euler.pdf','ipm.pdf','statement.pdf',"I'm thinking about the P vs NP problem.md",'pnp p2 .md','pnp 3.md','millennium-analysis-report.md','pnp-network-architecture-analysis.md','millennium-analysis-thread-receipt.json']
    missing=[]
    for name in names:
        src=home/'Downloads'/name
        if src.exists():copy(src,'sources/documents/'+name,'supplied_or_generated_document')
        else:missing.append(name)
    for src in sorted((home/'Downloads/millennium-analysis-private').glob('*.txt')):
        copy(src,'sources/extracted/'+src.name,'pdf_text_extraction')
    repo=home/'pnp-network-architecture'
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()
    files=subprocess.check_output(['git','ls-files'],cwd=repo,text=True).splitlines()
    for name in files:copy(repo/name,'experiment/'+name,'committed_experiment_snapshot')
    # Available delegation summaries referenced by this exact session.
    strings='\n'.join((r['content'] or '') for r in all_rows)
    summary_names=sorted(set(re.findall(r'subagent-summary-[\w.-]+\.txt',strings)))
    for name in summary_names:
        src=home/'.hermes/cache/delegation'/name
        if src.exists():copy(src,'sources/reviews/'+name,'delegation_summary')
    reads=sorted(set(clean(p) for p in document_reads if p))
    put('sources/read-inventory.json',json.dumps(reads,indent=2)+'\n','stored tool arguments','direct_read_inventory_not_exhaustive')
    manifest=dict(schema='session-review-v1',session_id=args.session,cutoff_message_id=args.cutoff,
                  cutoff='User request to export session; archive-construction messages excluded',experiment_commit=commit,
                  sessions=counts,missing_documents=missing,operational_skill_results_omitted=skill_count,
                  historical_web_extractions=web_count,files=entries,
                  limitations=['No system/developer prompts or hidden reasoning exported','All available permitted rows up to cutoff retained, including inactive/compacted/replayed rows','Truncated stored content cannot be reconstructed and is not silently completed','Skill bodies excluded; research documents included','Third-party redistribution rights and prose privacy review pending','Source documents copied from current disk, not asserted to equal historical versions unless hashes agree','Web files are historical tool extractions, not newly fetched full pages','No global session database or unrelated session export included'])
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:manifest[k] for k in ('sessions','missing_documents','historical_web_extractions','operational_skill_results_omitted')},indent=2))
    print('archived files',len(entries),'bytes',sum(e['bytes'] for e in entries))

if __name__=='__main__':main()
