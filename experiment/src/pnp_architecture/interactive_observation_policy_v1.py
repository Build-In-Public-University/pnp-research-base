from dataclasses import dataclass
@dataclass(frozen=True)
class HiddenState:
 name:str; visible:tuple; energy:float
STATES=(HiddenState('low_power',('same_time','same_cpu','same_bytes'),1.0),HiddenState('high_power',('same_time','same_cpu','same_bytes'),2.0))
POLICIES={'passive':('passive',),'privileged':('passive','privileged'),'calibration':('passive','calibrate')}
COST={'passive':1,'privileged':3,'calibrate':10}
def step(s,action):
 if action=='passive':return s.visible
 if action=='privileged':return s.visible+('energy='+str(s.energy),)
 if action=='calibrate':return ('calibrated_energy_class='+('low' if s.energy<1.5 else 'high'),)
 raise ValueError(action)
def transcript(s,policy):return tuple((a,step(s,a)) for a in POLICIES[policy])
def analyze(policy):
 ts={s.name:transcript(s,policy) for s in STATES};ident=ts['low_power']!=ts['high_power'];return {'policy':policy,'identifiable':ident,'transcripts':ts,'observation_cost':sum(COST[a] for a in POLICIES[policy]),'measurement_perturbation':policy!='passive'}
def experiment():return {'states':[s.__dict__ for s in STATES],'policies':{p:analyze(p) for p in POLICIES},'energy_units':'synthetic'}
