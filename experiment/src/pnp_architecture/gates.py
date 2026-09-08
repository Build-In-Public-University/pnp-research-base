"""Real predicates with declared synthetic invocation prices; no runtime claim."""
from collections import Counter

COSTS = {'syntax': 1, 'local': 2, 'composition': 5}
ORDERS = [('syntax', 'local', 'composition'), ('syntax', 'composition', 'local')]
TEMPLATES = {
    'valid': {'payload': [1, 2], 'target': 3},
    'syntax': {'payload': 'bad', 'target': 3},
    'local': {'payload': [-1, 2], 'target': 1},
    'composition': {'payload': [1, 2], 'target': 4},
    'both': {'payload': [-1, 2], 'target': 4},
}
WORKLOADS = {
    'local_heavy': {'valid': 10, 'syntax': 10, 'local': 70, 'composition': 10},
    'composition_heavy': {'valid': 10, 'syntax': 10, 'local': 10, 'composition': 70},
    'all_valid': {'valid': 100},
    'correlated': {'valid': 10, 'syntax': 10, 'local': 10, 'composition': 10, 'both': 60},
}


def gate(name, candidate):
    if name == 'syntax':
        return (type(candidate.get('payload')) is list
                and all(type(x) is int for x in candidate['payload'])
                and type(candidate.get('target')) is int)
    if name == 'local':
        return all(x >= 0 for x in candidate['payload'])
    if name == 'composition':
        return sum(candidate['payload']) == candidate['target']
    raise ValueError(name)


def run_pipeline(candidate, order=ORDERS[0], full=False):
    if tuple(order) not in ORDERS:
        raise ValueError('All gates required; syntax must precede dependent predicates')
    calls, outcomes = [], []
    for name in order:
        calls.append(name)
        ok = gate(name, candidate)
        outcomes.append(ok)
        if not ok and (not full or name == 'syntax'):
            break
    return {'accepted': len(calls) == 3 and all(outcomes),
            'calls': calls, 'outcomes': outcomes,
            'modeled_cost': sum(COSTS[g] for g in calls)}


def oracle(candidate):
    """Separate imperative oracle, not a conjunction of the gate function calls."""
    payload = candidate.get('payload')
    if type(payload) is not list or type(candidate.get('target')) is not int:
        return False
    total = 0
    for x in payload:
        if type(x) is not int or x < 0:
            return False
        total += x
    return total == candidate['target']


def experiment():
    workloads = []
    for name, mix in WORKLOADS.items():
        candidates = [dict(TEMPLATES[k]) for k, count in mix.items() for _ in range(count)]
        gold = [oracle(c) for c in candidates]
        policies = []
        for label, order, full in [('cheap_first', ORDERS[0], False),
                                   ('composition_first', ORDERS[1], False),
                                   ('full_checks', ORDERS[0], True)]:
            rows = [run_pipeline(c, order, full) for c in candidates]
            reached = Counter(g for row in rows for g in row['calls'])
            modeled_cost = sum(row['modeled_cost'] for row in rows)
            assert [r['accepted'] for r in rows] == gold
            policies.append({'name': label, 'order': list(order), 'full': full,
                             'modeled_cost': modeled_cost,
                             'mean_modeled_cost': modeled_cost / len(candidates),
                             'reached': dict(reached), 'gate_calls': sum(reached.values()),
                             'accepted': sum(r['accepted'] for r in rows), 'rows': rows})
        best_cost = min(p['modeled_cost'] for p in policies[:2])
        workloads.append({'name': name, 'mix': mix, 'candidates': candidates, 'oracle': gold,
                          'policies': policies,
                          'retrospective_best_legal_orders': [p['name'] for p in policies[:2]
                                                               if p['modeled_cost'] == best_cost]})
    learned = workloads[0]['retrospective_best_legal_orders'][0]
    target = workloads[1]
    transferred = next(p for p in target['policies'] if p['name'] == learned)
    return {'status': 'executed_predicates_with_declared_model_prices',
            'cost_units': 'synthetic invocation points, NOT runtime or energy',
            'costs': COSTS, 'workloads': workloads,
            'transfer': {'selection_workload': 'local_heavy', 'evaluation_workload': 'composition_heavy',
                         'frozen_policy': learned, 'modeled_cost': transferred['modeled_cost'],
                         'target_oracle_cost': min(p['modeled_cost'] for p in target['policies'][:2]),
                         'selection_cost_included': False,
                         'boundary': 'Retrospective order reference, not an online optimizer or deployment measurement'}}
