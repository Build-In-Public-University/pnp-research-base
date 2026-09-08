"""Finite contract-relative information audit. Not a novelty or complexity claim."""
from itertools import product


def response_map(observations, allowed, feasible):
    """Construct one feasible answer per attained observation, or report impossible.

    allowed[s] and feasible are bitmasks over three actions. The construction
    uses the declared possible-world model, not the hidden actual state.
    """
    if (not observations or len(observations) != len(allowed)
            or any(o not in (0,1) for o in observations)
            or any(mask not in range(8) for mask in allowed)
            or feasible not in range(8)):
        raise ValueError('Invalid finite observation/contract/action model')
    intersections = {}
    for observation, mask in zip(observations, allowed):
        intersections[observation] = intersections.get(observation, feasible) & mask
    if any(mask == 0 for mask in intersections.values()):
        return None
    return {o: next(a for a in range(3) if mask & (1 << a))
            for o,mask in intersections.items()}


def enumerate_oracle(observations, allowed, feasible):
    # Independent enumerate-and-check oracle; no grouping/intersection logic.
    for mapping in product(range(3), repeat=2):
        if all(((1 << mapping[observations[s]]) & allowed[s] & feasible) != 0
               for s in range(len(observations))):
            return True
    return False


def experiment():
    binary = {'cases': 0, 'sufficient': 0, 'insufficient': 0, 'disagreements': 0}
    for observation in product((0,1), repeat=4):
        for target in product((0,1), repeat=4):
            fiber_constant = all(observation[i] != observation[j] or target[i] == target[j]
                                 for i in range(4) for j in range(4))
            exists = any(all(mapping[observation[s]] == target[s] for s in range(4))
                         for mapping in product((0,1), repeat=2))
            binary['cases'] += 1
            binary['sufficient' if exists else 'insufficient'] += 1
            binary['disagreements'] += fiber_constant != exists
    relational = {'cases': 0, 'feasible': 0, 'infeasible': 0, 'disagreements': 0}
    for observation in product((0,1), repeat=3):
        for allowed in product(range(8), repeat=3):
            for feasible in range(8):
                mapping = response_map(observation, allowed, feasible)
                exists = enumerate_oracle(observation, allowed, feasible)
                relational['cases'] += 1
                relational['feasible' if exists else 'infeasible'] += 1
                relational['disagreements'] += (mapping is not None) != exists
                if mapping is not None:
                    assert all((1 << mapping[o]) & feasible & mask
                               for o,mask in zip(observation, allowed))
    assert binary['disagreements'] == relational['disagreements'] == 0
    return {'status': 'executed_finite_information_boundary_audit',
            'binary': binary, 'relational': relational,
            'enumeration': {'binary_states': 4, 'relational_states': 3,
                            'observation_labels': [0,1], 'actions': [0,1,2],
                            'allowed_and_feasible_masks': list(range(8))},
            'witnesses': {
                'pairwise_but_not_joint': {'observations': [0,0,0], 'allowed_masks': [3,6,5],
                                          'feasible_mask': 7, 'response': response_map([0,0,0],[3,6,5],7)},
                'deferral_permitted': {'observations': [0,0], 'allowed_masks': [5,6],
                                      'feasible_mask': 7, 'response': response_map([0,0],[5,6],7)},
                'deferral_denied': {'observations': [0,0], 'allowed_masks': [5,6],
                                   'feasible_mask': 3, 'response': response_map([0,0],[5,6],3)},
                'threshold_sufficient': {'possible_states': [48,49], 'predicate': 's < 50',
                                         'observations': [0,0], 'required': [True,True]},
                'threshold_insufficient': {'possible_states': [48,49,50], 'predicate': 's < 50',
                                           'observations': [0,0,0], 'required': [True,True,False]}},
            'boundary': 'Finite exhaustive checks illustrate standard indistinguishability. '
                        'No claim of efficient computation of observation, model, or response map; '
                        'no wall-clock, sensor, AI, P/NP or novel-theorem result.'}
