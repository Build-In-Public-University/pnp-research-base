SETUPS={'fresh':0,'persistent_remote':8,'local_replica':15}
INVOKE={'fresh':11,'persistent_remote':3,'local_replica':1}
def totals(n):return {k:SETUPS[k]+INVOKE[k]*n for k in SETUPS}
def best(n):
 t=totals(n);return min(t,key=lambda k:(t[k],k))
def experiment(max_n=12):
 rows=[]
 for n in range(1,max_n+1):
  t=totals(n);rows.append({'n':n,'totals':t,'averages':{k:t[k]/n for k in t},'best':best(n)})
 return {'rows':rows,'setups':SETUPS,'invocation_costs':INVOKE,'units':'synthetic modeled cost','crossover_remote_local':'n>3.5'}
