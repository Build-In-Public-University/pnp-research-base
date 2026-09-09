from dataclasses import dataclass
@dataclass(frozen=True)
class State:
 name:str;first:str;second:str
STATES=(State('A','easy_A','unused'),State('B','easy_B','unused'),State('C','uncertain','local_C'),State('D','uncertain','local_D'),State('E','uncertain','local_uncertain'))
COST={'cheap_local':1,'second_local':2,'privileged_exact':6}
PRIOR={s.name:1/len(STATES) for s in STATES}
def adaptive_transcript(s):
 out=[('cheap_local',s.first)]
 if s.first=='easy_A' or s.first=='easy_B':return tuple(out)
 out.append(('second_local',s.second))
 if s.second=='local_uncertain':out.append(('privileged_exact',s.name))
 return tuple(out)
def cost(t):return sum(COST[a] for a,_ in t)
def analyze():
 ts={s.name:adaptive_transcript(s) for s in STATES}; costs={n:cost(t) for n,t in ts.items()}
 return {'transcripts':ts,'cost_by_state':costs,'worst_cost':max(costs.values()),'expected_cost':sum(PRIOR[n]*c for n,c in costs.items()),'identifiable':len(set(ts.values()))==len(STATES),'prior':PRIOR,'always_privileged_cost':6}
def experiment():return {'states':[s.__dict__ for s in STATES],'channels':COST,'policy':analyze(),'energy_units':'synthetic modeled cost'}
