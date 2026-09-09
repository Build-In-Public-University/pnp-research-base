import itertools,math

def observe(mask,event,n):return mask==0 if event=='inspect' else None
def update(mask,event,n):
 if event.startswith('satisfy_'):return mask & ~(1<<int(event[8:]))
 if event.startswith('invalidate_'):return mask | (1<<int(event[10:]))
 return mask
def run(mask,seq,n):
 out=[]
 for e in seq:out.append(observe(mask,e,n));mask=update(mask,e,n)
 return tuple(out),mask
def shortest(a,b,n):
 if a==b:return None
 if (a==0)!=(b==0):return 1
 return min(a.bit_count(),b.bit_count())+1
def analyze(n):
 states=list(range(1<<n));pairs=[shortest(a,b,n) for a,b in itertools.combinations(states,2)]
 depths=[x for x in pairs if x is not None]
 return {'n':n,'K_G':len(states),'I_G_bits':math.ceil(math.log2(len(states))),'reachable_states':len(states),'pair_count':len(pairs),'all_pairwise_distinguishable':all(x is not None for x in pairs),'max_distinguishing_depth':max(depths) if depths else 0,'mean_distinguishing_depth':sum(depths)/len(depths) if depths else 0,'update_work_per_event':1,'decision_work_per_query':n,'evidence_state_bits':n}
def experiment(ns=range(1,9)):return {'family':'n-bit unresolved-obligation masks','rows':[analyze(n) for n in ns],'claims':{'K_G':'2^n','I_G_bits':'n','update_work':'1 bit touched','decision_work':'n-bit scan'}}
