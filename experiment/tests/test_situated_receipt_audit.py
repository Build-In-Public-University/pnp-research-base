"""Independent post-run audits of retained situated-computation receipts.

No experiment implementation imports: reconstruct received state, counters and
oracle outcomes directly from artifacts. These are post-hoc audit tests, not
claimed as prospective behavioral RED coverage for the experiments.
"""
from collections import Counter
import hashlib
import itertools
import json
import math
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

def read(name):
    return json.loads((ROOT/'artifacts'/name).read_text())

class SituatedReceiptAudit(unittest.TestCase):
    def test_replay_and_sources(self):
        pairs=[('information_v1.json','information_v1-repeat.json'),
               ('observation_v1.json','observation_v1-repeat.json'),
               ('release_v1_run1.json','release_v1_run2.json'),
               ('release_v1_run1.md','release_v1_run2.md')]
        for a,b in pairs:
            self.assertEqual((ROOT/'artifacts'/a).read_bytes(),(ROOT/'artifacts'/b).read_bytes())
        for name in ('information_v1.json','observation_v1.json','release_v1_run1.json','release_v1_verified1.json'):
            r=read(name)
            hashes=r.get('source_sha256') or r['provenance']['sha256']
            for p,h in hashes.items():
                # Original test source is archived verbatim: post-run lint removed
                # two unused imports only. Never relabel the original provenance.
                actual=ROOT/'artifacts/release_v1-test-source.txt' if name=='release_v1_run1.json' and p=='tests/test_release.py' else ROOT/p
                self.assertEqual(hashlib.sha256(actual.read_bytes()).hexdigest(),h,p)
        old=read('release_v1_run1.json'); reviewed=read('release_v1_verified1.json')
        old['provenance']['sha256']['tests/test_release.py']=reviewed['provenance']['sha256']['tests/test_release.py']
        self.assertEqual(old,reviewed)
        self.assertEqual((ROOT/'artifacts/release_v1_verified1.json').read_bytes(),(ROOT/'artifacts/release_v1_verified2.json').read_bytes())

    def test_observation_received_state_and_all_counters(self):
        r=read('observation_v1.json')
        worlds={w['id']:w for w in r['worlds']}
        for cell in r['cells']:
            world=worlds[cell['world_id']]
            n=cell['n']; threshold=cell['threshold']
            for policy,p in cell['policies'].items():
                cache=[None]*n
                counted=Counter(); payload=Counter(); seq=0
                for t in p['ticks']:
                    tick=t['tick']; c=t['counters']; observed=t['observed']
                    new_seq=seq+len(world['updates'][tick])
                    if policy=='event_log':
                        published=[[i+seq+1,*e] for i,e in enumerate(world['updates'][tick])]
                        received=[e for e in published if cell['transport']=='complete' or e[0]%5]
                        self.assertEqual(received,observed['events'])
                        self.assertEqual(observed['checkpoint'],[tick,new_seq])
                    else:
                        self.assertEqual(observed['events'],[])
                        self.assertIsNone(observed['checkpoint'])
                    writes=0; squares=0; initialization=0
                    def replace(i,value):
                        nonlocal writes,squares,initialization
                        if all(v is None for v in cache): initialization+=1
                        squares+=1+(cache[i] is not None)
                        writes+=1
                        cache[i]=value
                    for _,i,value in observed['events']: replace(i,value)
                    for snapshot in observed['snapshots']:
                        self.assertEqual(snapshot[0],tick)
                        self.assertEqual(snapshot[2:],world['states'][tick])
                        for i,value in enumerate(snapshot[2:]):
                            if cache[i]!=value:replace(i,value)
                    self.assertEqual(cache,t['cache'])
                    truth=world['states'][tick] if cell['contract']=='exact' else sum(v*v for v in world['states'][tick])>=threshold
                    self.assertEqual(t['truth'],truth)
                    self.assertEqual(t['wrong'],t['output'] is not None and t['output']!=truth)
                    intervals=[list(range(max(-8,v-t['age']),min(8,v+t['age'])+1)) for v in cache]
                    for domain,actual in zip(intervals,world['states'][tick]):self.assertIn(actual,domain)
                    lo=sum(min(v*v for v in d) for d in intervals)
                    hi=sum(max(v*v for v in d) for d in intervals)
                    sufficient=all(len(d)==1 for d in intervals) if cell['contract']=='exact' else (lo>=threshold)==(hi>=threshold)
                    self.assertEqual(sufficient,t['evidence_sufficient'])
                    if t['guaranteed']:
                        self.assertTrue(sufficient)
                        self.assertEqual(t['output'],truth)
                    bound=policy=='poll_guarded' and t['age']>0
                    expected=Counter({k:0 for k in c})
                    expected['source_write']=len(world['updates'][tick])
                    if policy=='event_log':
                        expected['source_sequence']=len(world['updates'][tick])
                        expected['source_log_field']=3*len(world['updates'][tick])
                        expected['source_checkpoint_field']=2
                        expected['sequence_check']=2+len(observed['events'])
                    snapshots=len(observed['snapshots'])
                    expected['source_snapshot_field']=snapshots*(n+2)
                    expected['snapshot_compare']=snapshots*n
                    expected['sequence_check']+=snapshots
                    expected['cache_write']=writes
                    expected['producer_publish_field']=expected['source_log_field']+expected['source_checkpoint_field']+expected['source_snapshot_field']
                    expected['delivery_field']=expected['producer_publish_field']
                    expected['receive_field']=3*len(observed['events'])+(2 if observed['checkpoint'] is not None else 0)+snapshots*(n+2)
                    expected['schedule_check']=int(policy.startswith('poll_'))
                    expected['interval_coordinate']=n if bound else 0
                    if cell['contract']=='threshold':
                        expected['calculation_square']=squares+(2*n if bound else 0)
                        expected['calculation_total_write']=writes+initialization+(2+2*n if bound else 0)
                        expected['contract_check']=1+int(lo<threshold) if bound else 1
                        self.assertEqual(t['cached_total'],sum(v*v for v in cache))
                    expected['output_field']=(n if cell['contract']=='exact' else 1) if t['output'] is not None else 0
                    self.assertEqual(dict(expected),c,(cell,policy,tick))
                    self.assertEqual(t['payload']['sent_fields'],expected['producer_publish_field'])
                    self.assertEqual(t['payload']['delivered_fields'],expected['receive_field'])
                    self.assertEqual(t['payload']['dropped_fields'],expected['producer_publish_field']-expected['receive_field'])
                    counted.update(c); payload.update(t['payload']); seq=new_seq
                self.assertEqual(dict(counted),p['counters'])
                self.assertEqual(dict(payload),p['payload'])
                self.assertEqual(sum(counted.values()),p['operations'])
                self.assertEqual(p['emitted']+p['unavailable'],len(p['ticks']))
                self.assertEqual(p['wrong_emitted'],sum(t['wrong'] for t in p['ticks']))
                self.assertEqual(p['guaranteed_emitted'],sum(t['guaranteed'] and t['output'] is not None for t in p['ticks']))
            eligible={name:p['operations'] for name,p in cell['policies'].items()
                      if p['guaranteed_emitted']==len(p['ticks']) and not p['wrong_emitted']}
            self.assertEqual(set(cell['full_service_guaranteed_winners']),{name for name,cost in eligible.items() if cost==min(eligible.values())})

    def test_release_oracle_costs_and_exposure(self):
        r=read('release_v1_run1.json')
        fixtures={json.dumps(f['cell'],sort_keys=True):f for f in r['fixtures']}
        ops=('domain_tests','pair_tests','modulo','sum_additions','local_tests','metadata_tests','auth_ops')
        for row in r['rows']:
            f=fixtures[json.dumps(row['cell'],sort_keys=True)]
            truth=[]
            for a in f['current']:
                v=a['vector']
                valid=all(type(x)is int and x>=2 for x in v) and all(math.gcd(x,y)==1 for x,y in itertools.combinations(v,2))
                truth.append([valid and sum(v)<=budget for budget in f['budgets']])
            self.assertEqual(truth,row['oracle'])
            if row['policy'] in ('broad','gate','attested'):self.assertEqual(truth,row['decisions'])
            falseaccept=sum(d is True and not target for ds,ts in zip(row['decisions'],truth) for d,target in zip(ds,ts))
            self.assertEqual(falseaccept,row['false_accept'])
            self.assertEqual(sum(row['false_accept_fanout']),falseaccept)
            compute=sum(row[stage][key] for stage in ('upstream','downstream') for key in ops)
            total=compute+sum(row[stage][key] for stage in ('upstream','downstream') for key in ('hash_bytes','auth_message_bytes'))+sum(row['communication'].values())
            self.assertEqual(compute,row['compute_only']); self.assertEqual(total,row['total_unit_weight'])
            self.assertEqual(sum(row['checks_per_candidate']),row['shared_checks'])
            self.assertEqual(sum(max(0,c-1) for c in row['checks_per_candidate']),row['duplicate_shared_checks'])
            if row['policy']=='broad':self.assertEqual(row['exposure'],len(f['current'])*len(f['budgets']))
            if row['policy'] in ('gate','attested'):
                valid_original=sum(all(math.gcd(x,y)==1 for x,y in itertools.combinations(a['vector'],2)) for a in f['original'])
                self.assertEqual(row['exposure'],valid_original*len(f['budgets']))
