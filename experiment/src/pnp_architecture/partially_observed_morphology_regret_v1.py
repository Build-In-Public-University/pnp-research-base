from fractions import Fraction
import random,hashlib,json
T=12;SEED=0;SW=4
EM={'low':{.5:Fraction(4,10),1.5:Fraction(6,10)},'high':{.5:Fraction(6,10),1.5:Fraction(4,10)}}
def op(m,d):return 3*d if m=='remote' else d+2
def posterior(p,d):
 a=p*EM['high'].get(d,0);b=(1-p)*EM['low'].get(d,0);return a/(a+b) if a+b else p
def obs_prob(p,d):return p*EM['high'].get(d,0)+(1-p)*EM['low'].get(d,0)
def bayes_value():
 from functools import lru_cache
 @lru_cache(None)
 def v(t,m,p):
  if t==T:return 0
  total=Fraction(0)
  for d in set(EM['low'])|set(EM['high']):
   q=obs_prob(p,d)
   if not q:continue
   pn=posterior(p,d);choices=[]
   for target in ('remote','local'):
    choices.append((Fraction(str(op(target,d)))+(SW if target!=m else 0)+v(t+1,target,pn),target))
   total+=q*min(choices,key=lambda x:(x[0],x[1]))[0]
  return total
 return v
def path():
 r=random.Random(SEED);theta='high' if r.random()<.5 else 'low';ds=[]
 for _ in range(T):
  u=r.random();cum=0
  for d,q in EM[theta].items():
   cum+=float(q)
   if u<cum:ds.append(d);break
 return theta,ds
def realized_opt(ds):
 n=len(ds);dp={(n,m):0. for m in ('remote','local')};ch={}
 for t in range(n-1,-1,-1):
  for m in ('remote','local'):
   vals=[(op(x,ds[t])+(SW if x!=m else 0)+dp[(t+1,x)],x) for x in ('remote','local')];dp[(t,m)],ch[(t,m)]=min(vals,key=lambda x:(x[0],x[1]))
 return dp[(0,'remote')]
def run():
 theta,ds=path();p=Fraction(1,2);m='remote';heur=bayes=0.;trace=[];bv=bayes_value()
 for t,d in enumerate(ds):
  pn=posterior(p,d);hv='local' if d>1 else 'remote';opts=[]
  for target in ('remote','local'):
   cost=op(target,d)+(SW if target!=m else 0);future=0.
   # after this observation, v expects next observation
   future=float(bv(t+1,target,pn));opts.append((cost+future,target))
  target=min(opts,key=lambda x:(x[0],x[1]))[1];heur+=op(hv,d)+(SW if hv!=m else 0);bayes+=op(target,d)+(SW if target!=m else 0);trace.append({'t':t,'d':d,'posterior_high':float(pn),'heuristic':hv,'bayes':target});m=target;p=pn
 clair=realized_opt(ds)
 return {'seed':SEED,'hidden_regime':theta,'demand_path':ds,'demand_path_sha256':hashlib.sha256(json.dumps(ds).encode()).hexdigest(),'cost_heuristic':heur,'cost_bayes':bayes,'cost_clairvoyant':clair,'policy_regret':heur-bayes,'uncertainty_regret':bayes-clair,'structural_regret':heur-clair,'trace':trace}
