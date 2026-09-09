from dataclasses import dataclass
from itertools import permutations
@dataclass(frozen=True)
class State:
 name:str;parity:int;group:int
STATES=(State('A',0,0),State('B',1,0),State('C',0,1),State('D',1,1))
COST={'passive':0,'local_parity':1,'local_group':3,'privileged_exact':6}
def observe(s,a):
 if a=='passive':return 'nominal'
 if a=='local_parity':return s.parity
 if a=='local_group':return s.group
 if a=='privileged_exact':return s.name
 raise ValueError(a)
def transcript(s,actions):return tuple((a,observe(s,a)) for a in actions)
def identifiable(actions):return len({transcript(s,actions) for s in STATES})==len(STATES)
def search():
 candidates=[]
 for length in range(1,4):
  for actions in permutations(('local_parity','local_group','privileged_exact'),length):
   candidates.append((sum(COST[a] for a in actions),actions,identifiable(actions)))
 return sorted(candidates,key=lambda x:(x[0],len(x[1]),x[1]))
def experiment():
 ranked=search();best=next(x for x in ranked if x[2]);return {'states':[s.__dict__ for s in STATES],'channels':COST,'best_policy':{'actions':best[1],'cost':best[0],'identifiable':best[2]},'candidates':[{'actions':x[1],'cost':x[0],'identifiable':x[2]} for x in ranked],'passive_identifiable':identifiable(('passive',)),'energy_units':'synthetic modeled cost'}
