"""Bounded, deterministic executed algorithms; see frozen docs/protocol-v2.md.

Counters are algorithm-specific operations, not timing/energy measurements.
All parallelism is simulated serially. Historical model.py is not used here.
"""
from collections import deque
import hashlib
from itertools import product
import json
from pathlib import Path
import random

CONFIG = {
    'network_sizes': [1, 2, 4, 8, 16, 32],
    'payload_bits': [8, 16, 32, 64],
    'topologies': ['chain', 'star', 'balanced_tree', 'complete', 'disconnected'],
    'reuse_counts': [1, 4, 16],
    'sat_variables': [4, 6, 8, 10, 12],
    'replicates': [0, 1, 2],
    'seed_base': 20260908,
    'seed_rule': 'seed_base + 100*n + replicate',
    'random_clause_multiplier': 4,
    'assignment_order': 'ascending integer; variable i = bit i',
    'processor_rule': ['1', 'n', '2**n'],
    'flood_policy': 'forward once to all neighbors including sender',
    'root': 0,
}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def graph(kind, n):
    if n < 1 or kind not in CONFIG['topologies']:
        raise ValueError('unknown topology or nonpositive node count')
    g = [set() for _ in range(n)]
    if kind == 'chain':
        pairs = [(i - 1, i) for i in range(1, n)]
    elif kind == 'star':
        pairs = [(0, i) for i in range(1, n)]
    elif kind == 'balanced_tree':
        pairs = [((i - 1) // 2, i) for i in range(1, n)]
    elif kind == 'complete':
        pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    else:
        pairs = [(i - 1, i) for i in range(1, n) if i != n // 2]
    for u, v in pairs:
        g[u].add(v)
        g[v].add(u)
    return tuple(tuple(sorted(neighbors)) for neighbors in g)


def edges(g):
    return [(u, v) for u, neighbors in enumerate(g) for v in neighbors if u < v]


def reachability_oracle(g):
    """Independent fixed-point edge closure, not the BFS or message engine."""
    reached = {0}
    while True:
        grown = reached | {v for u in reached for v in g[u]}
        if grown == reached:
            return sorted(reached)
        reached = grown


def bfs_tree(g):
    tree = [[] for _ in g]
    parent: list[int | None] = [None for _ in g]
    seen = {0}
    queue = deque([0])
    inspections = 0
    while queue:
        u = queue.popleft()
        for v in g[u]:
            inspections += 1
            if v not in seen:
                seen.add(v)
                parent[v] = u
                tree[u].append(v)
                queue.append(v)
    return tuple(tuple(children) for children in tree), parent, inspections


def propagate(g, payload):
    """Synchronous first-arrival engine for undirected flood or directed tree."""
    if not g or any(bit not in '01' for bit in payload):
        raise ValueError('nonempty graph and binary payload required')
    received = {0: payload}
    frontier = [0]
    sends = bit_hops = rounds = last_arrival = 0
    while frontier:
        messages = []
        for u in sorted(frontier):
            for v in g[u]:
                messages.append((v, received[u]))
                sends += 1
                bit_hops += len(received[u])
        if not messages:
            break
        rounds += 1
        frontier = []
        for v, message in messages:
            if v not in received:
                received[v] = message
                frontier.append(v)
                last_arrival = rounds
    exact = all(message == payload for message in received.values())
    return {'sends': sends, 'payload_bit_hops': bit_hops, 'rounds': rounds,
            'delivery_rounds': last_arrival, 'reached': sorted(received),
            'reached_count': len(received), 'reached_payloads_exact': exact,
            'all_reached_exact': len(received) == len(g) and exact}


def reuse_propagation(g, payload, repeats):
    if repeats < 1:
        raise ValueError('positive reuse count required')
    tree, _, inspections = bfs_tree(g)
    result = {'repeats': repeats, 'bfs_setup_inspections': inspections}
    for name, network in [('flood', g), ('routed', tree)]:
        total = dict.fromkeys(['sends', 'payload_bit_hops', 'rounds', 'delivery_rounds'], 0)
        total['all_reached_exact'] = True
        for _ in range(repeats):
            r = propagate(network, payload)
            for key in ['sends', 'payload_bit_hops', 'rounds', 'delivery_rounds']:
                total[key] += r[key]
            total['all_reached_exact'] &= r['all_reached_exact']
        result[name] = total
    return result


def containing(g, bits):
    if len(bits) != len(g) or not g:
        raise ValueError('one submitted bit per node required')
    local = []
    local_inspections = 0
    for bit in bits:
        local_inspections += 1
        local.append(bit in (0, 1))
    # Independent oracle never uses received messages or tree structure.
    oracle = set(bits) in ({0}, {1})
    tree, parent, setup = bfs_tree(g)
    reached = reachability_oracle(tree)
    collected = {0: bits[0]}
    pending = [(u, u, bits[u]) for u in reached if u != 0]
    sends = rounds = 0
    while pending:
        rounds += 1
        next_pending = []
        for origin, position, bit in pending:
            destination = parent[position]
            sends += 1
            if destination == 0:
                collected[origin] = bit
            else:
                next_pending.append((origin, destination, bit))
        pending = next_pending
    comparisons = central_local_inspections = 0
    valid = True
    for bit in collected.values():
        central_local_inspections += 1
        valid = (bit in (0, 1)) and valid
    if len(collected) != len(g):
        status, agrees = 'unavailable', None
    else:
        for node in sorted(collected):
            if node != 0:
                comparisons += 1
                valid = (collected[node] == collected[0]) and valid
        status = 'accept_witness' if valid else 'reject_witness'
        agrees = valid == oracle
    return {
        'bits': list(bits), 'oracle_global_valid': oracle, 'problem_status': 'SAT',
        'problem_status_reason': 'all-zero witness exists; submitted witness rejection is not UNSAT',
        'local_only': {'local_results': local, 'local_inspections': local_inspections,
                       'all_local_valid': all(local), 'global_decision': 'not_evaluated',
                       'naive_global_prediction': all(local),
                       'naive_global_prediction_correct': all(local) == oracle},
        'centralized': {'status': status, 'agrees_with_oracle': agrees,
                        'received': len(collected), 'sends': sends,
                        'payload_bit_hops': sends, 'rounds': rounds,
                        'local_inspections': central_local_inspections,
                        'equality_comparisons': comparisons, 'bfs_setup_inspections': setup},
    }


def random_cnf(n, seed):
    if n < 3:
        raise ValueError('three distinct variables required')
    rng = random.Random(seed)
    return [tuple((v + 1) * (1 if rng.randrange(2) else -1)
                  for v in rng.sample(range(n), 3)) for _ in range(4 * n)]


def unsat_core():
    return [tuple((i + 1) * (1 if sign else -1) for i, sign in enumerate(signs))
            for signs in product((False, True), repeat=3)]


def verify_cnf(formula, assignment):
    inspections = 0
    for clause in formula:
        clause_true = False
        for literal in clause:
            inspections += 1
            bit = bool((assignment >> (abs(literal) - 1)) & 1)
            if bit == (literal > 0):
                clause_true = True
                break
        if not clause_true:
            return False, inspections
    return True, inspections


def cnf_oracle(formula, assignment):
    """Independent full literal sums; no verifier short-circuit or work reuse."""
    clause_sums = [sum(((assignment // (2 ** (abs(lit) - 1))) % 2)
                       if lit > 0 else 1 - ((assignment // (2 ** (abs(lit) - 1))) % 2)
                       for lit in clause) for clause in formula]
    return min(clause_sums, default=1) > 0


def exhaustive(formula, n):
    table, costs = [], []
    for assignment in range(1 << n):
        valid, cost = verify_cnf(formula, assignment)
        if valid != cnf_oracle(formula, assignment):
            raise AssertionError('verifier disagrees with independent oracle')
        table.append('1' if valid else '0')
        costs.append(cost)
    return {'truth_table': ''.join(table), 'candidate_work': costs,
            'literal_inspections': sum(costs), 'satisfying_count': table.count('1'),
            'oracle_agreement': True}


def schedule(formula, n, processors):
    if n < 0 or processors < 1:
        raise ValueError('invalid scheduler size')
    batches = candidates = total_work = makespan = 0
    witness = None
    for start in range(0, 1 << n, processors):
        work, winners = [], []
        batches += 1
        for assignment in range(start, min(start + processors, 1 << n)):
            valid, inspections = verify_cnf(formula, assignment)
            candidates += 1
            total_work += inspections
            work.append(inspections)
            if valid:
                winners.append(assignment)
        makespan += max(work)
        if winners:
            witness = min(winners)
            break
    verified, verification_work = (None, 0) if witness is None else verify_cnf(formula, witness)
    return {'processors': processors, 'batches': batches, 'candidates': candidates,
            'total_work': total_work, 'idealized_makespan': makespan,
            'status': 'SAT' if witness is not None else 'UNSAT', 'witness': witness,
            'witness_verified': verified, 'verification_inspections': verification_work,
            'real_parallel_hardware_used': False}


def run_suite(root):
    root = Path(root)
    protocol_bytes = (root / 'docs/protocol-v2.md').read_bytes()
    protocol_hash = hashlib.sha256(protocol_bytes).hexdigest()
    if protocol_hash != (root / 'docs/protocol-v2.sha256').read_text().split()[0]:
        raise ValueError('frozen protocol hash mismatch')
    paths = ['src/pnp_architecture/experiments_v2.py', 'scripts/run_experiments_v2.py',
             'tests/test_experiments_v2.py', 'tests/test_model.py', 'src/pnp_architecture/cli.py',
             'src/pnp_architecture/model.py', 'artifacts/first_attack.json',
             'docs/protocol-v2.md', 'docs/protocol-v2.sha256']
    source_hashes = {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in paths}
    graphs, propagation, constraints, formulas = [], [], [], []
    for kind in CONFIG['topologies']:
        for n in CONFIG['network_sizes']:
            g = graph(kind, n)
            identity = {'topology': kind, 'N': n, 'edges': edges(g), 'root': 0}
            identity['sha256'] = digest(identity)
            graphs.append(identity)
            tree, _, setup = bfs_tree(g)
            oracle = reachability_oracle(g)
            for length in CONFIG['payload_bits']:
                payload = '0' * length
                flood, routed = propagate(g, payload), propagate(tree, payload)
                if flood['reached'] != oracle or routed['reached'] != oracle:
                    raise AssertionError('propagation reachability disagreement')
                propagation.append({'graph_sha256': identity['sha256'], 'topology': kind,
                                    'N': n, 'payload_bits': length, 'payload': payload,
                                    'flood': flood, 'routed': routed,
                                    'bfs_setup_inspections': setup, 'oracle_reached': oracle,
                                    'oracle_agreement': True,
                                    'reuse': [reuse_propagation(g, payload, k) for k in CONFIG['reuse_counts']]})
            for label, bits in [('zeros', [0] * n), ('single_one', [0] * (n - 1) + [1])]:
                row = containing(g, bits)
                if row['centralized']['agrees_with_oracle'] is False:
                    raise AssertionError('containing oracle mismatch')
                row.update({'case': label, 'topology': kind, 'N': n, 'graph_sha256': identity['sha256'],
                            'input_sha256': digest({'graph': identity['sha256'], 'bits': bits})})
                constraints.append(row)
    for n in CONFIG['sat_variables']:
        for replicate in CONFIG['replicates']:
            seed = CONFIG['seed_base'] + 100 * n + replicate
            random_formula = random_cnf(n, seed)
            for variant in ['random', 'random_plus_unsat_core']:
                formula = random_formula + (unsat_core() if variant != 'random' else [])
                full = exhaustive(formula, n)
                schedules = [schedule(formula, n, p) for p in [1, n, 1 << n]]
                for row in schedules:
                    expected_witness = full['truth_table'].find('1')
                    if row['witness'] != (None if expected_witness < 0 else expected_witness):
                        raise AssertionError('scheduler disagrees with truth table')
                    if row['total_work'] != sum(full['candidate_work'][:row['candidates']]):
                        raise AssertionError('scheduler work accounting mismatch')
                    expected_span = sum(max(full['candidate_work'][i:min(i + row['processors'], row['candidates'])])
                                        for i in range(0, row['candidates'], row['processors']))
                    if row['idealized_makespan'] != expected_span:
                        raise AssertionError('scheduler makespan mismatch')
                    row['oracle_agreement'] = True
                if variant != 'random' and full['satisfying_count']:
                    raise AssertionError('UNSAT core failed')
                # Header stores n and m in their unsigned binary widths. Each literal
                # stores one sign bit and a fixed-width zero-based variable index.
                literal_width = 1 + (n - 1).bit_length()
                identity = {'n': n, 'seed': seed, 'replicate': replicate,
                            'variant': variant, 'clauses': formula}
                formulas.append({**identity, 'input_sha256': digest(identity),
                                 'clause_count': len(formula), 'literal_count': 3 * len(formula),
                                 'encoding_bits': n.bit_length() + len(formula).bit_length() + 3 * len(formula) * literal_width,
                                 'encoding': 'unsigned n,m headers; sign + ceil(log2(n)) variable bits per literal',
                                 'exhaustive': full, 'schedules': schedules})
    return {'protocol': 'pnp-network-architecture-v2', 'status': 'executed_synthetic_algorithms',
            'protocol_sha256': protocol_hash, 'source_sha256': source_hashes,
            'config': CONFIG, 'config_sha256': digest(CONFIG), 'graphs': graphs,
            'propagation': propagation, 'containing_constraint': constraints, 'cnf': formulas,
            'limitations': [
                'Finite synthetic graphs/formulas only; no universal or P/NP separation claims.',
                'No real parallel hardware used; makespan is idealized literal-inspection scheduling.',
                'No real timing, energy, contention, headers, failures, graph generation or memory costs.',
                'BFS is centralized setup; its adjacency inspections are not network message counts.',
                'CNF search excludes assignment generation, formula replication, orchestration and oracle work.',
                'UNSAT is established here by exhaustive enumeration, not inferred from a rejected witness.',
                'Input size includes clause count and literals; brute-force observations are not SAT lower bounds.',
                'first_attack.json is preserved arithmetic-only bookkeeping, not an executed verifier.',
            ]}


def summary_markdown(data):
    lines = ['# Executed bounded experiments v2', '',
             'Generated from the deterministic JSON receipt; synthetic algorithms only.',
             f"Frozen protocol SHA-256: `{data['protocol_sha256']}`", '',
             f"Rows: {len(data['graphs'])} explicit graphs, {len(data['propagation'])} propagation cells, "
             f"{len(data['containing_constraint'])} containing witnesses, {len(data['cnf'])} CNF formulas.", '',
             '## Propagation: N=32, payload=64 bits, one use', '',
             '| Topology | Flood sends | Flood rounds | Tree sends | Tree rounds | BFS inspections | All reached |',
             '|---|---:|---:|---:|---:|---:|---|']
    for r in data['propagation']:
        if r['N'] == 32 and r['payload_bits'] == 64:
            lines.append(f"| {r['topology']} | {r['flood']['sends']} | {r['flood']['rounds']} | "
                         f"{r['routed']['sends']} | {r['routed']['rounds']} | {r['bfs_setup_inspections']} | {r['routed']['all_reached_exact']} |")
    lines += ['', 'Sends are measured loop events; bit-hops count payload bits on each hop. Flood rounds',
              'include redundant final transmissions. Routing eliminates dense redundant sends, not setup',
              'inspections or depth. Connected tree routes tie in send counts, a useful negative result.',
              'Reuse totals execute each repetition; setup is charged once, separately, not added to messages.', '',
              '## Containing constraint', '']
    rows = data['containing_constraint']
    lines += [f"Naive local-only false global predictions: {sum(not r['local_only']['naive_global_prediction_correct'] for r in rows)}.",
              f"Centralized accepted/rejected/unavailable: {sum(r['centralized']['status'] == 'accept_witness' for r in rows)}/"
              f"{sum(r['centralized']['status'] == 'reject_witness' for r in rows)}/"
              f"{sum(r['centralized']['status'] == 'unavailable' for r in rows)}.",
              f"Available centralized/oracle disagreements: {sum(r['centralized']['agrees_with_oracle'] is False for r in rows)}.",
              'All containing problems remain satisfiable; rejections concern submitted witnesses.',
              'Singleton single-one inputs are consistent. Disconnected non-singletons are unavailable.', '',
              '## CNF: individual n=12 runs (all sizes and full truth tables in JSON)', '',
              '| Variant | Replicate | Clauses | Satisfying assignments | p | Candidates | Work | Idealized makespan |',
              '|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in data['cnf']:
        if r['n'] == 12:
            for s in r['schedules']:
                lines.append(f"| {r['variant']} | {r['replicate']} | {r['clause_count']} | {r['exhaustive']['satisfying_count']} | "
                             f"{s['processors']} | {s['candidates']} | {s['total_work']} | {s['idealized_makespan']} |")
    sat = [r for r in data['cnf'] if r['exhaustive']['satisfying_count']]
    lines += ['', f"SAT formulas: {len(sat)}; UNSAT formulas: {len(data['cnf']) - len(sat)}.",
              f"SAT formulas where p=2**n uses more work than p=1: {sum(r['schedules'][2]['total_work'] > r['schedules'][0]['total_work'] for r in sat)}.",
              'Every schedule matched the independent exhaustive truth table and accounting checks.',
              'All candidates in the winning batch were charged, including candidates after first success.',
              'Large processor budgets trade idealized depth for work; this is not a faster hardware measurement.', '',
              '## Limitations', '']
    lines += ['- ' + limit for limit in data['limitations']]
    return '\n'.join(lines) + '\n'
