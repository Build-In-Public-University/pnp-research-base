from typing import Iterator
from heapq import heappop,heappush
State=tuple[str,frozenset[str],bool,bool,bool]
START:State=('i',frozenset({'parity'}),False,False,False)
GOAL=frozenset({'parity','group'})
ACTIONS={'discover':1,'move':5,'connect':2,'transfer':2,'compose':1}
def next_states(state:State)->Iterator[tuple[str,State]]:
 loc,caps,known,linked,done=state
 if not known:yield ('discover',(loc,caps,True,linked,done))
 if known and loc=='i':yield ('move',('j',caps,known,linked,done))
 if known and loc=='j' and not linked:yield ('connect',('j',caps,known,True,done))
 if known and linked and 'group' not in caps:yield ('transfer',('j',caps|{'group'},known,linked,done))
 if caps==GOAL and not done:yield ('compose',(loc,caps,known,linked,True))
def shortest():
 q:list[tuple[int,int,State,tuple[str,...]]]=[(0,0,START,())];seen:dict[State,int]={START:0};serial=0
 while q:
  cost,_,s,path=heappop(q)
  if s[-1]:return cost,path,s
  for a,ns in next_states(s):
   nc=cost+ACTIONS[a]
   if nc<seen.get(ns,10**9):seen[ns]=nc;serial+=1;heappush(q,(nc,serial,ns,path+(a,)))
 raise RuntimeError('no route')
def experiment():
 cost,path,state=shortest();return {'start':START,'goal':sorted(GOAL),'best_cost':cost,'best_path':path,'final_state':state,'capability_acquisition':state[1]==GOAL,'actions':ACTIONS,'discovery_changes_capabilities':False,'transfer_changes_capabilities':True}
