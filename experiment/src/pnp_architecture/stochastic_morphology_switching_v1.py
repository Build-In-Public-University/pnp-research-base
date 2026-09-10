import random,hashlib,json
T=500;SEED=1337;DS=(.1,1.0,4.0)
def path():
 r=random.Random(SEED);i=1;out=[]
 for _ in range(T):
  out.append(DS[i]);u=r.random();i=(i+1)%3 if u<.1 else (i-1)%3 if u<.2 else i
 return out
def run(ds,name,enter,exit,switch):
 m='remote';cost=0;operate=0;transition=0;sw=0;entries=0;exits=0;occ={'remote':0,'local':0}
 for d in ds:
  target='local' if d>enter else 'remote' if d<exit else m
  if name=='stateless':target='local' if d>1 else 'remote'
  if target!=m:
   transition+=switch[(m,target)];sw+=1;entries+=target=='local';exits+=target=='remote';m=target
  charge=3*d if m=='remote' else d+2;operate+=charge;cost+=charge;occ[m]+=1
 return {'cost':cost+transition,'operating_cost':operate,'transition_cost':transition,'switches':sw,'entries':entries,'exits':exits,'occupancy':occ}
def experiment():
 ds=path();res={'stateless':run(ds,'stateless',1,1, {('remote','local'):2,('local','remote'):2}),'symmetric':run(ds,'symmetric',1.25,.75,{('remote','local'):2,('local','remote'):2}),'adaptive':run(ds,'adaptive',2.25,.25,{('remote','local'):10,('local','remote'):6})};fixed={'remote':sum(3*d for d in ds),'local':sum(d+2 for d in ds)};base=min(fixed.values());
 for x in res.values():x['regret_vs_best_fixed']=x['cost']-base
 return {'seed':SEED,'periods':T,'demand_path_sha256':hashlib.sha256(json.dumps(ds).encode()).hexdigest(),'agents':res,'fixed_baseline':fixed,'best_fixed_cost':base,'demands':list(DS),'units':'synthetic modeled cost'}
