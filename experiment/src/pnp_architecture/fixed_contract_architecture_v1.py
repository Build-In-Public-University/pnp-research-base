import math

def oracle(mask,event,n):
 if event.startswith('satisfy_'):return mask & ~(1<<int(event[8:]))
 if event.startswith('invalidate_'):return mask | (1<<int(event[11:]))
 return mask
class Raw:
 def __init__(self,n):self.n=n;self.mask=0
 def event(self,e):self.mask=oracle(self.mask,e,self.n);return 1
 def decision(self):return self.mask==0
class Counter(Raw):
 def __init__(self,n):super().__init__(n);self.count=0
 def event(self,e):
  before=self.mask;super().event(e);self.count+=(self.mask.bit_count()-before.bit_count());return 1
 def decision(self):return self.count==0
class Sparse:
 def __init__(self,n):self.n=n;self.unresolved=set()
 def event(self,e):
  i=int(e[8:] if e.startswith('satisfy_') else e[11:]);
  if e.startswith('satisfy_'):self.unresolved.discard(i)
  elif e.startswith('invalidate_'):self.unresolved.add(i)
  return 1
 def decision(self):return not self.unresolved
class EventLog:
 def __init__(self,n):self.n=n;self.log=[]
 def event(self,e):self.log.append(e);return 1
 def decision(self):
  mask=0
  for e in self.log:mask=oracle(mask,e,self.n)
  return mask==0
def workload(n):return [f'invalidate_{i}' for i in range(n)]+[f'satisfy_{i}' for i in reversed(range(n))]+['inspect']
def analyze(n):
 rows=[];seq=workload(n)
 for name,cls in [('raw_mask',Raw),('mask_counter',Counter),('sparse_set',Sparse),('event_log',EventLog)]:
  a=cls(n);mask=0;exact=True;u=o=0
  for e in seq:
   if e=='inspect':continue
   mask=oracle(mask,e,n);u+=a.event(e);o+=1;exact &= a.decision()==(mask==0)
  exact &= a.decision()==(mask==0)
  bits=math.ceil(math.log2(n)) if n>1 else 1
  mem={'raw_mask':n,'mask_counter':n+math.ceil(math.log2(n+1)),'sparse_set':n*bits,'event_log':len(seq)*math.ceil(math.log2(2*n+1))}[name]
  decision={'raw_mask':n,'mask_counter':1,'sparse_set':1,'event_log':len(seq)}[name]
  rows.append({'architecture':name,'n':n,'exact':exact,'retained_bits':mem,'update_work':u,'observation_work':o,'decision_work':decision,'evidence_work':{'raw_mask':0,'mask_counter':1,'sparse_set':1,'event_log':2}[name]})
 return rows
def experiment(ns=range(1,9)):return {'contract':'n-bit unresolved-obligation mask, fixed across architectures','rows':[r for n in ns for r in analyze(n)],'workload':'invalidate all, satisfy all in reverse order, inspect','cost_note':'modeled units; sparse memory is worst-case fixed-width index estimate'}
