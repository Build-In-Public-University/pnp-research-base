import math
from pnp_architecture.dual_control_policy_phase_diagram_v1 import costs,best
def entropy(p):return -(p*math.log2(p)+(1-p)*math.log2(1-p)) if p not in (0,1) else 0.0
def report(p):
 stop=100*min(p,1-p);perfect=0.0;return {'p':p,'entropy_bits':entropy(p),'stop_risk':stop,'perfect_information_residual_risk':perfect,'voi_perfect_information':stop-perfect,'costs':costs(p),'best_policy':best(p)}
def experiment():return {'beliefs':{'p_0.1':report(.1),'p_0.9':report(.9)},'constants':{'wrong_loss':100,'correct_action_cost':1,'touch_total_base':2,'touch_damage_per_fragile':10,'inspect_total':6},'units':'synthetic modeled cost'}
