import statistics,hashlib,json
import pnp_architecture.partially_observed_morphology_regret_v1 as one
N=100
def experiment():
 rows=[]
 for seed in range(N):
  one.SEED=seed;r=one.run();rows.append({'seed':seed,'policy_regret':r['policy_regret'],'uncertainty_regret':r['uncertainty_regret'],'structural_regret':r['structural_regret'],'heuristic':r['cost_heuristic'],'bayes':r['cost_bayes'],'clairvoyant':r['cost_clairvoyant']})
 one.SEED=0
 def stats(k):
  x=[r[k] for r in rows];return {'mean':statistics.mean(x),'median':statistics.median(x),'min':min(x),'max':max(x)}
 total=sum(r['structural_regret'] for r in rows);policy=sum(r['policy_regret'] for r in rows);unc=sum(r['uncertainty_regret'] for r in rows)
 return {'seeds':N,'rows':rows,'summary':{k:stats(k) for k in ('policy_regret','uncertainty_regret','structural_regret')},'aggregate_policy_share':policy/total,'aggregate_uncertainty_share':unc/total,'telescoping_failures':sum(r['structural_regret']!=r['policy_regret']+r['uncertainty_regret'] for r in rows)}
