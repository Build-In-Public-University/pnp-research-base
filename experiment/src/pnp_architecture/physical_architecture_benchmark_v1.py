import random,time,tracemalloc,statistics,math,platform,sys
class Base:
 def __init__(self,n):self.n=n;self.reads=0;self.writes=0
 def reset_counts(self):self.reads=self.writes=0
class Raw(Base):
 def __init__(self,n):super().__init__(n);self.mask=0
 def update(self,i,kind):self.mask=(self.mask|1<<i) if kind else (self.mask&~(1<<i));self.reads+=1;self.writes+=1
 def query(self):
  x=self.mask;self.reads+=self.n//8+1;return x==0
class Counter(Raw):
 def __init__(self,n):super().__init__(n);self.count=0
 def update(self,i,kind):
  old=(self.mask>>i)&1;new=int(kind);super().update(i,kind);self.count+=new-old;self.writes+=1
 def query(self):self.reads+=1;return self.count==0
class Sparse(Base):
 def __init__(self,n):super().__init__(n);self.s=set()
 def update(self,i,kind):
  if kind:self.s.add(i)
  else:self.s.discard(i)
  self.reads+=1;self.writes+=1
 def query(self):self.reads+=8;return not self.s
class Log(Base):
 def __init__(self,n):super().__init__(n);self.log=[]
 def update(self,i,kind):self.log.append((i,kind));self.writes+=8
 def query(self):
  s=set()
  for i,k in self.log:
   if k:s.add(i)
   else:s.discard(i)
  self.reads+=8*len(self.log);return not s
ARCH=[('raw_mask',Raw),('mask_counter',Counter),('sparse_set',Sparse),('event_log',Log)]
def stream(n,ratio,seed):
 rng=random.Random(seed);updates=max(8,n//16);queries=max(1,round(updates*ratio));return [(rng.randrange(n),rng.randrange(2)) for _ in range(updates)],queries
def case(n,ratio,seed,reps=3):
 updates,queries=stream(n,ratio,seed);rows=[]
 for name,cls in ARCH:
  times=[];cpus=[];peaks=[];last=None
  for rep in range(reps):
   a=cls(n);a.reset_counts();tracemalloc.start();w0=time.perf_counter_ns();c0=time.process_time_ns()
   for i,k in updates:a.update(i,k)
   answers=[a.query() for _ in range(queries)]
   c1=time.process_time_ns();w1=time.perf_counter_ns();_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
   times.append(w1-w0);cpus.append(c1-c0);peaks.append(peak);last=(a,answers)
  oracle=Log(n);[oracle.update(i,k) for i,k in updates];expected=[oracle.query() for _ in range(queries)]
  rows.append({'n':n,'query_update_ratio':ratio,'architecture':name,'exact':last[1]==expected,'updates':len(updates),'queries':queries,'wall_ns_median':statistics.median(times),'cpu_ns_median':statistics.median(cpus),'tracemalloc_peak_bytes_median':statistics.median(peaks),'logical_read_bytes':last[0].reads,'logical_write_bytes':last[0].writes,'repetitions':reps})
 return rows
def benchmark(ns=(128,512,2048,8192),ratios=(.1,1,10,100),seed=260909):
 return {'python':sys.version.split()[0],'platform':platform.platform(),'seed':seed,'rows':[r for n in ns for q in ratios for r in case(n,q,seed+n+round(q*1000))]}
