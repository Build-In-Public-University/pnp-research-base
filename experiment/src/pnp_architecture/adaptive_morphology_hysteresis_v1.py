from functools import lru_cache
SW={('remote','local'):10,('local','remote'):6,('remote','remote'):0,('local','local'):0}
def running(m,d):return 3*d if m=='remote' else d+2
@lru_cache(None)
def dp(m,d,h):
 if h==0:return (0,())
 opts=[]
 for nm in ('remote','local'):
  tail,path=dp(nm,d,h-1);opts.append((running(nm,d)+SW[(m,nm)]+tail,(nm,)+path))
 return min(opts,key=lambda x:(x[0],x[1]))
def experiment():
 ds=[0,.1,.25,.5,1,2,2.25,3,4,8];rows=[]
 for d in ds:
  for m in ('remote','local'):
   cost,path=dp(m,d,4);rows.append({'d':d,'start':m,'cost':cost,'policy':path})
 return {'rows':rows,'horizon':4,'switch_costs':SW,'running_costs':{'remote':'3d','local':'d+2'},'units':'synthetic modeled cost'}
