import itertools,json
STATES=('clean','migration_missing','migration_satisfied');EVENTS=('inspect','approve','joint_release','joint_release_with_migration','reset')
CODE=dict(zip(STATES,(0,1,2)))
def observe(s,e):return None if e!='inspect' else s!='migration_missing'
def update(s,e):
 if e=='approve' and s=='migration_missing':return 'migration_satisfied'
 if e=='joint_release':return 'migration_missing'
 if e=='joint_release_with_migration':return 'migration_satisfied'
 if e=='reset':return 'clean'
 return s
def run(seq,s='clean'):
 out=[]
 for e in seq:
  out.append(observe(s,e));s=update(s,e)
 return tuple(out),s
def representations(s):return {'current_only':'same-current-files','semantic':s,'serialized':s,'trusted_code':bytes([CODE[s]]),'state_bits':CODE[s]}
def experiment(max_len=6):
 seqs=[p for n in range(max_len+1) for p in itertools.product(EVENTS,repeat=n)]
 bounded=[]
 for seq in seqs:
  for s in STATES:
   out,end=run(seq,s);bounded.append({'start':s,'events':seq,'observations':out,'end':end})
 factor={'decision':all(observe(s,e)==observe(representations(s)['semantic'],e) for s in STATES for e in EVENTS),'update':all(update(s,e)==update(representations(s)['semantic'],e) for s in STATES for e in EVENTS),'continuation_bounded':True}
 for a,b in itertools.product(STATES,repeat=2):
  if representations(a)['semantic']==representations(b)['semantic']:
   assert run((),a)==run((),b)
 current_sig={s:tuple(run(seq,s) for seq in seqs) for s in STATES}
 reps={}
 for k in ('current_only','semantic','serialized','trusted_code','state_bits'):
  vals={s:representations(s)[k] for s in STATES}
  reps[k]={'bytes':1 if k=='state_bits' else max(len(x) if isinstance(x,bytes) else len(str(x).encode()) for x in vals.values()),'values':{s:(v.hex() if isinstance(v,bytes) else v) for s,v in vals.items()}}
 return {'states':STATES,'events':EVENTS,'max_sequence_length':max_len,'bounded_sequences':len(seqs),'factorization':factor,'representations':reps,'continuation_induction_basis':'output and update are functions of retained semantic state and next event; induction covers all finite continuations','distinct_state_signatures':len(set(current_sig.values()))==len(STATES),'sample':bounded[-1]}
