SETUP={'fresh':0,'remote':8,'local':15}
def totals(n,lam):return {'fresh':11*n,'remote':8+3*n,'local':15+n+12*lam*n}
def best(n,lam):
 t=totals(n,lam);return min(t,key=lambda k:(t[k],k))
def experiment():
 lambdas=[0,.05,.1,.2,.4];rows=[]
 for lam in lambdas:
  for n in range(1,13):rows.append({'n':n,'lambda':lam,'totals':totals(n,lam),'best':best(n,lam)})
 return {'rows':rows,'lambdas':lambdas,'demand_range':[1,12],'refresh_validation_per_invocation_per_lambda':12,'units':'synthetic expected cost'}
