from dataclasses import dataclass
@dataclass(frozen=True)
class State: name:str
STATES=(State('fragile'),State('sturdy'))
WRONG=100;CORRECT=1;INSPECT=5;TOUCH=1;DAMAGE=10
def costs(p):
 immediate=CORRECT+min(p,1-p)*WRONG
 inspect=INSPECT+CORRECT
 touch=TOUCH+CORRECT+p*DAMAGE
 vals={'act_immediately':immediate,'inspect_then_act':inspect,'gentle_touch_then_act':touch}
 best=sorted(vals,key=lambda name:vals[name])[0]
 return {'fragile_prior':p,'values':vals,'best_policy':best,'best_cost':vals[best],'touch_observes':True,'touch_changes_state':True}
def experiment():return {'scenarios':{'rare_fragile':costs(.1),'common_fragile':costs(.5)},'constants':{'wrong_action_loss':WRONG,'correct_action_cost':CORRECT,'inspect_cost':INSPECT,'touch_cost':TOUCH,'touch_damage':DAMAGE},'units':'synthetic modeled cost'}
