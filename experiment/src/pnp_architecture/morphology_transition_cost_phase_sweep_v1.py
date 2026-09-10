import math,random,hashlib,json
T=500;SEED=2026;DS=(.1,1.0,4.0);SWEEP=(0,2,6,10,20);H=4
def demand_path():
    r=random.Random(SEED)
    return [1+1.35*math.sin(i*.17)+.18*(r.random()-.5) for i in range(T)]
def operating(m,d): return 3*d if m=='remote' else d+2
def simulate(ds,srl,slr):
    m='remote';op=tr=0.;switches=entries=exits=lock=0;occ={'remote':0,'local':0}
    enter=1+srl/(2*H); exit=1-slr/(2*H)
    for d in ds:
        target='local' if d>enter else 'remote' if d<exit else m
        if target!=m:
            tr += srl if target=='local' else slr; switches+=1; entries+=target=='local'; exits+=target=='remote'; m=target
        op += operating(m,d);occ[m]+=1
        lock += int((m=='local' and d<1) or (m=='remote' and d>1))
    return {'S_RL':srl,'S_LR':slr,'enter_threshold':enter,'exit_threshold':exit,'total_cost':op+tr,'operating_cost':op,'transition_cost':tr,'switches':switches,'entries':entries,'exits':exits,'occupancy':occ,'lock_in_periods':lock,'lock_in_rate':lock/len(ds)}
def optimal(ds,srl,slr):
    morph=('remote','local');n=len(ds);dp={(n,m):0. for m in morph};choice={}
    for t in range(n-1,-1,-1):
        for current in morph:
            candidates=[]
            for target in morph:
                transition=0 if target==current else (srl if target=='local' else slr)
                candidates.append((operating(target,ds[t])+transition+dp[(t+1,target)],target))
            dp[(t,current)],choice[(t,current)]=min(candidates,key=lambda x:(x[0],x[1]))
    m='remote';op=tr=0.;switches=lock=0;occ={'remote':0,'local':0};path=[]
    for t,d in enumerate(ds):
        target=choice[(t,m)];path.append(target)
        if target!=m:tr+=srl if target=='local' else slr;switches+=1;m=target
        op+=operating(m,d);occ[m]+=1;lock+=int((m=='local' and d<1) or (m=='remote' and d>1))
    return {'optimal_cost':op+tr,'optimal_operating_cost':op,'optimal_transition_cost':tr,'optimal_switches':switches,'optimal_lock_in_rate':lock/n,'optimal_occupancy':occ,'optimal_path_sha256':hashlib.sha256(json.dumps(path).encode()).hexdigest()}
def experiment():
    ds=demand_path();fixed={'remote':sum(operating('remote',d) for d in ds),'local':sum(operating('local',d) for d in ds)};base=min(fixed.values());rows=[]
    for a in SWEEP:
        for b in SWEEP:
            x=simulate(ds,a,b);x.update(optimal(ds,a,b));x['regret_vs_best_fixed']=x['total_cost']-base;x['regret_vs_optimal']=x['total_cost']-x['optimal_cost'];x['behavioral_lock_in']=x['lock_in_rate']>0;x['optimal_lock_in']=x['optimal_lock_in_rate']>0;rows.append(x)
    return {'seed':SEED,'periods':T,'horizon':H,'sweep':list(SWEEP),'demand_path_sha256':hashlib.sha256(json.dumps(ds).encode()).hexdigest(),'fixed_baseline':fixed,'best_fixed_cost':base,'rows':rows,'units':'synthetic modeled cost'}
