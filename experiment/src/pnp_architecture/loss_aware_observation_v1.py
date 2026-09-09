from dataclasses import dataclass
@dataclass(frozen=True)
class State:
 name:str;first:str;second:str;truth:str
STATES=(State('A','easy','unused','safe'),State('B','easy','unused','safe'),State('C','uncertain','clear','safe'),State('D','uncertain','residual','safe'),State('E','uncertain','residual','escalate'))
COST={'cheap':1,'local':2,'privileged':6}
def obs(s,a):
 if a=='cheap':return s.first
 if a=='local':return s.second
 if a=='privileged':return s.name
 raise ValueError(a)
def posterior(states,prior,events):
 kept=[s for s in states if all(obs(s,a)==o for a,o in events)];z=sum(prior[s.name] for s in kept);return {s.name:prior[s.name]/z for s in kept}
def stop_risk(p,loss):
 ps=sum(v for n,v in p.items() if n=='E');return min(ps,1-ps)*loss
def policy(prior,loss):
 events=[('cheap','uncertain')];p=posterior(STATES,prior,events);after_local={o:posterior(STATES,prior,events+[('local',o)]) for o in ('clear','residual')};
 residual=after_local['residual'];stop=stop_risk(residual,loss);observe=COST['privileged'];decision='observe_privileged' if observe<stop else 'stop_safe'
 return {'prior':prior,'loss':loss,'residual_posterior':residual,'residual_stop_risk':stop,'privileged_cost':observe,'residual_choice':decision,'first_cost':COST['cheap'],'local_cost':COST['local'],'policy_expected_cost':COST['cheap']+sum(prior[s.name] for s in STATES if s.first=='uncertain')*COST['local']+sum(prior[s.name] for s in STATES if s.first=='uncertain' and s.second=='residual')*(observe if decision=='observe_privileged' else stop),'exact_identification':False}
def experiment():
 common={s.name:0.2 for s in STATES};rare={'A':.49,'B':.49,'C':.01,'D':.009,'E':.001};return {'scenarios':{'common_high_loss':policy(common,20),'rare_low_loss':policy(rare,20)},'states':[s.__dict__ for s in STATES],'energy_units':'synthetic modeled cost'}
