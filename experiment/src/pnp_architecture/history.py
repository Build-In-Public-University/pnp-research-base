"""Bounded dynamic computation. Counters are a declared unit-cost proxy, not time."""
from collections import Counter
from fractions import Fraction
import hashlib
import json
import random

POLICIES = ('cold', 'incremental_snapshot', 'unchecked', 'incremental_feed')
PENALTIES = (0, 10, 100, 1000, 10000)


def dependencies(n):
    return [tuple((i+j) % n for j in range(4)) for i in range(n)]


def oracle(state):
    # Independent closed-index calculation; not the engine's evaluate function.
    n = len(state)
    values = [sum(state[(i+j) % n] ** 2 for j in range(4)) for i in range(n)]
    total = sum(values)
    return {'values': values, 'total': total, 'accepted': total <= 4*n}


class Engine:
    def __init__(self, policy, initial):
        if policy not in POLICIES or len(initial) < 4:
            raise ValueError('Unknown policy or too few variables')
        self.policy, self.n = policy, len(initial)
        self.deps = dependencies(self.n)
        c = Counter()
        self.cached = None
        self.reverse = None
        if policy.startswith('incremental'):
            self.cached = []
            for value in initial:
                c['input_read'] += 1
                self.cached.append(value)
                c['snapshot_write'] += 1
            self.reverse = [[] for _ in initial]
            for i, dep in enumerate(self.deps):
                for j in dep:
                    c['dependency_read'] += 1
                    self.reverse[j].append(i)
                    c['index_write'] += 1
        self.result = self.recompute(initial, c)
        self.initial_counters = dict(c)

    def evaluate(self, state, i, c):
        value = 0
        for j in self.deps[i]:
            c['dependency_read'] += 1
            x = state[j]
            c['input_read' if state is not self.cached else 'snapshot_read'] += 1
            squared = x*x
            c['multiply'] += 1
            value += squared
            c['add'] += 1
        return value

    def recompute(self, state, c):
        values = []
        for i in range(self.n):
            values.append(self.evaluate(state, i, c))
            c['output_write'] += 1
        total = 0
        for y in values:
            c['output_read'] += 1
            total += y
            c['add'] += 1
        c['predicate'] += 1
        return {'values': values, 'total': total, 'accepted': total <= 4*self.n}

    def update(self, state, feed):
        c = Counter()
        if self.policy == 'cold':
            self.result = self.recompute(state, c)
            return dict(c)
        c['cache_lookup'] += 1
        if self.policy == 'unchecked':
            return dict(c)
        assert self.cached is not None and self.reverse is not None
        dirty = set()
        if self.policy == 'incremental_snapshot':
            observed = enumerate(state)
        else:
            observed = iter(feed)
        for j, value in observed:
            c['input_read' if self.policy == 'incremental_snapshot' else 'feed_read'] += 1
            old = self.cached[j]
            c['snapshot_read'] += 1
            c['compare'] += 1
            if value != old:
                self.cached[j] = value
                c['snapshot_write'] += 1
                for i in self.reverse[j]:
                    c['index_read'] += 1
                    dirty.add(i)
                    c['dirty_mark'] += 1
        # Only cached state is consulted here: omitted events cannot leak oracle input.
        for i in dirty:
            old = self.result['values'][i]
            c['output_read'] += 1
            new = self.evaluate(self.cached, i, c)
            self.result['values'][i] = new
            c['output_write'] += 1
            c['total_read'] += 2
            self.result['total'] -= old
            c['subtract'] += 1
            self.result['total'] += new
            c['add'] += 1
            c['total_write'] += 2
        c['predicate'] += 1
        self.result['accepted'] = self.result['total'] <= 4*self.n
        return dict(c)

    def retained_slots(self):
        # Declared application state scalars/references, not heap byte measurement.
        # Shared fixed dependency input and transient working state excluded.
        if self.policy == 'cold':
            return 0
        slots = self.n + 2  # output vector, total, acceptance
        if self.cached is not None:
            assert self.reverse is not None
            slots += self.n + sum(len(x) for x in self.reverse) + self.n
        return slots


def trajectory(n, k, seed, steps=32):
    rng = random.Random(seed)
    state = [0]*n
    out = [{'state': list(state), 'events': []}]
    for _ in range(steps):
        changed = sorted(rng.sample(range(n), k))
        for j in changed:
            state[j] = (state[j]+1) % 4
        out.append({'state': list(state), 'events': [(j, state[j]) for j in changed]})
    return out


def surface(policies):
    exact = {name: p for name, p in policies.items() if p['wrong_outputs'] == 0}
    exact_best = min(p['operations'] for p in exact.values())
    rows = []
    for penalty in PENALTIES:
        costs = {name: p['operations'] + penalty*p['wrong_outputs'] for name,p in policies.items()}
        best = min(costs.values())
        rows.append({'penalty_per_wrong_output': penalty, 'costs': costs,
                     'winners': [name for name,c in costs.items() if c == best]})
    thresholds = {}
    for name,p in policies.items():
        if p['wrong_outputs'] and exact_best > p['operations']:
            f = Fraction(exact_best-p['operations'], p['wrong_outputs'])
            thresholds[name] = {'numerator': f.numerator, 'denominator': f.denominator}
    return {'rows': rows, 'break_even_penalties': thresholds,
            'strict_correctness_winners': [name for name,p in exact.items() if p['operations'] == exact_best],
            'eligibility_boundary': 'Observed exactness on this trajectory only; not a future safety guarantee'}


def run_cell(n, k, seed, visibility):
    if visibility not in ('complete', 'omitted'):
        raise ValueError(visibility)
    world = trajectory(n,k,seed)
    policies = {}
    for name in POLICIES:
        engine = Engine(name, world[0]['state'])
        rows, totals = [], Counter()
        for t, event in enumerate(world):
            feed = event['events'] if visibility == 'complete' else [(j,v) for j,v in event['events'] if j % 2 == 0]
            counters = engine.initial_counters if t == 0 else engine.update(event['state'], feed)
            # Receipt copy is explicitly outside charged solver work.
            returned = {'values': list(engine.result['values']),
                        'total': engine.result['total'], 'accepted': engine.result['accepted']}
            truth = oracle(event['state'])
            wrong = returned != truth
            rows.append({'t': t, 'returned': returned, 'counters': counters,
                         'wrong_output': wrong,
                         'false_acceptance': returned['accepted'] and not truth['accepted'],
                         'false_rejection': not returned['accepted'] and truth['accepted']})
            totals.update(counters)
        policies[name] = {'steps': rows, 'counters': dict(totals), 'operations': sum(totals.values()),
                          'wrong_outputs': sum(r['wrong_output'] for r in rows),
                          'false_acceptances': sum(r['false_acceptance'] for r in rows),
                          'false_rejections': sum(r['false_rejection'] for r in rows),
                          'retained_state_slots': engine.retained_slots()}
    assert policies['cold']['wrong_outputs'] == policies['incremental_snapshot']['wrong_outputs'] == 0
    if visibility == 'complete':
        assert policies['incremental_feed']['wrong_outputs'] == 0
    inputs = [{'state': e['state'],
               'feed': e['events'] if visibility == 'complete' else [(j,v) for j,v in e['events'] if j%2 == 0],
               'oracle': oracle(e['state'])} for e in world]
    return {'n': n, 'updates_per_step': k, 'seed': seed, 'visibility': visibility,
            'world_sha256': hashlib.sha256(json.dumps(world, sort_keys=True).encode()).hexdigest(),
            'inputs': inputs, 'policies': policies, 'surface': surface(policies)}


def experiment():
    cells = [run_cell(n,k,seed,visibility) for n in (16,64) for k in (0,1,n//4,n)
             for seed in (1,7,19) for visibility in ('complete','omitted')]
    return {'status': 'executed_dynamic_computation_unit_cost_proxy', 'cells': cells,
            'penalties': PENALTIES,
            'counter_boundary': 'Listed reads/writes/arithmetic/comparisons/index visits/set insertion attempts. '
                                'Loop control, allocation, input generation, feed production, fixed dependency construction, '
                                'oracle evaluation and receipt serialization excluded. No runtime/energy claim.',
            'cost_boundary': 'Unit weights and wrong-output penalties are synthetic; observed correctness is separate.'}
