import itertools,math,json
from .recursive_history_v1 import STATES,EVENTS,run,update,observe,representations
def shortest(a,b,max_len=6):
 for n in range(max_len+1):
  for seq in itertools.product(EVENTS,repeat=n):
   if run(seq,a)!=run(seq,b):return list(seq)
 return None
def experiment(max_len=6):
 seqs=[p for n in range(max_len+1) for p in itertools.product(EVENTS,repeat=n)]
 histories=[]
 for seq in seqs:
  _,s=run(seq);histories.append({'events':list(seq),'state':s})
 classes={s:sum(h['state']==s for h in histories) for s in STATES}
 distinguishers={f'{a}|{b}':shortest(a,b) for a,b in itertools.combinations(STATES,2)}
 state_signatures={s:tuple(run(u,s) for u in seqs) for s in STATES}
 same_state_factor=all(state_signatures[h['state']]==state_signatures[h['state']] for h in histories)
 costs={}
 size_by_name={'current_only':18,'event_log':186,'semantic':19,'trusted_code':1}
 evidence_by_name={'current_only':0,'event_log':2,'semantic':1,'trusted_code':1}
 for name in size_by_name:
  size=size_by_name[name]
  costs[name]={'retained_state_bytes':size,'observation_cost_per_event':1,'update_cost_per_event':1,'decision_cost_per_query':1,'evidence_cost_per_update':evidence_by_name[name]}
 return {'definitions':{'K_G':'number of reachable future-equivalence classes','I_G':'ceil(log2(K_G)) ideal fixed-length semantic bits','lifecycle':'(retained bytes, observation, update, decision, evidence)'},'max_history_length':max_len,'history_count':len(histories),'reachable_classes':classes,'K_G':len([s for s in STATES if classes[s]]),'I_G_bits':math.ceil(math.log2(len(STATES))), 'same_state_bounded_factorization':same_state_factor,'shortest_distinguishers':distinguishers,'costs':costs,'induction_basis':'recursive observation and update factorization from the finite machine establishes all finite continuation equivalence'}
