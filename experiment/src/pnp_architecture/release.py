"""Matched LOCAL release experiment. Evidence is TRUSTED ATTESTATION, not proof.

The public HMAC fixture key simulates an authenticated issuer; it provides no
production security. Policies never receive oracle labels. See frozen protocol.
"""
from collections import Counter
from copy import deepcopy
import hashlib
import hmac
import itertools
import math
import random

SAFE = ('broad', 'gate', 'attested')
POLICIES = SAFE + ('skip_local', 'weak_upstream')
KEY = b'PUBLIC LAB FIXTURE ONLY - NOT A SECRET'
PREDICATE = 'pairwise-coprime-integers-ge2-v1'
OP_KEYS = ('domain_tests', 'pair_tests', 'modulo', 'sum_additions',
           'local_tests', 'metadata_tests', 'auth_ops')
BYTE_KEYS = ('hash_bytes', 'auth_message_bytes')
COUNTER_KEYS = OP_KEYS + BYTE_KEYS + ('shared_checks', 'reused', 'fallbacks')


def pack(value):
    import json
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()


def domain(vector, counts):
    for value in vector:
        counts['domain_tests'] += 1
        if type(value) is not int or value < 2:
            return False
    return True


def shared(vector, counts):
    """One identical early-exit Euclidean algorithm in every full validator."""
    counts['shared_checks'] += 1
    if not domain(vector, counts):
        return False
    for i, a in enumerate(vector):
        for b in vector[i + 1:]:
            counts['pair_tests'] += 1
            x, y = a, b
            while y:
                counts['modulo'] += 1
                x, y = y, x % y
            if x != 1:
                return False
    return True


def local(vector, budget, counts):
    total = 0
    for value in vector:
        total += value
        counts['sum_additions'] += 1
    counts['local_tests'] += 1
    return total <= budget


def digest(artifact, counts):
    payload = pack(artifact)
    counts['hash_bytes'] += len(payload)
    return hashlib.sha256(payload).hexdigest()


def authenticate(body, counts):
    payload = pack(body)
    counts['auth_ops'] += 1
    counts['auth_message_bytes'] += len(payload)
    return hmac.new(KEY, payload, hashlib.sha256).hexdigest()


def issue(artifact, counts):
    """Issuer assertion only: caller must have checked shared, unless a control."""
    body = {key: artifact[key] for key in ('dependency', 'version', 'scope')}
    body.update(digest=digest(artifact, counts), predicate=PREDICATE)
    return dict(body, mac=authenticate(body, counts))


def receive(artifact, budget, evidence, counts, skip_local=False):
    """Only current payload, current contract, attestation: no fixture/oracle."""
    if artifact is None or budget is None:
        return None
    applicable = False
    if evidence is not None:
        body = {k: v for k, v in evidence.items() if k != 'mac'}
        authentic = hmac.compare_digest(evidence.get('mac', ''), authenticate(body, counts))
        current_digest = digest(artifact, counts)
        checks = [body.get('digest') == current_digest,
                  body.get('predicate') == PREDICATE,
                  body.get('dependency') == artifact['dependency'],
                  body.get('version') == artifact['version'],
                  body.get('scope') == artifact['scope']]
        counts['metadata_tests'] += len(checks)
        applicable = authentic and all(checks)
    if applicable:
        counts['reused'] += 1
        shared_ok = True
    else:
        counts['fallbacks'] += 1
        shared_ok = shared(artifact['vector'], counts)
    return shared_ok and (skip_local or local(artifact['vector'], budget, counts))


def oracle(artifact, budget):
    """Independent math.gcd implementation; called only by post-hoc scoring."""
    if artifact is None or budget is None:
        return None
    v = artifact['vector']
    return (all(type(x) is int and x >= 2 for x in v)
            and all(math.gcd(a, b) == 1 for a, b in itertools.combinations(v, 2))
            and sum(v) <= budget)


def cells():
    for n, size, seed, validity, compatibility in itertools.product(
            (1, 4, 16, 64), (8, 32), (1, 7, 19), ('all', 'mixed'), ('all', 'half', 'none')):
        yield dict(n=n, size=size, seed=seed, validity=validity, local=compatibility, fault='none')
    for n, size, fault in itertools.product((4, 16), (8, 32),
            ('mutation', 'dependency', 'version', 'scope', 'local_contract')):
        yield dict(n=n, size=size, seed=7, validity='mixed', local='half', fault=fault)


def materialize(cell):
    """One common fixture per cell, including post-approval delivered faults."""
    primes = [x for x in range(101, 2000)
              if all(x % d for d in range(2, math.isqrt(x) + 1))]
    rng = random.Random(cell['seed'])
    originals = []
    for index in range(8):
        vector = rng.sample(primes, cell['size'])
        if cell['validity'] == 'mixed' and index % 2:
            vector[-1] = vector[0]
        originals.append(dict(vector=vector, dependency='dep-1', version=1, scope='release-lab'))
    current = deepcopy(originals)
    budgets = [100000 if cell['local'] == 'all' or
               (cell['local'] == 'half' and i % 2 == 0) else 0
               for i in range(cell['n'])]
    fault = cell['fault']
    if fault == 'mutation':
        current[0]['vector'][-1] = current[0]['vector'][0]
    elif fault == 'dependency':
        current[0]['dependency'] = 'dep-2'
    elif fault == 'version':
        current[0]['version'] = 2
    elif fault == 'scope':
        current[0]['scope'] = 'other-scope'
    elif fault == 'local_contract':
        budgets[0] = 0
    elif fault != 'none':
        raise ValueError(f'Unknown fault: {fault}')
    return dict(cell=dict(cell), original=originals, current=current, budgets=budgets)


def evaluate(fixture, policy):
    if policy not in POLICIES:
        raise ValueError(policy)
    up, down, comm = Counter(), Counter(), Counter()
    decisions, checks_per_candidate = [], []
    exposure = 0
    for original, current in zip(fixture['original'], fixture['current']):
        before = up['shared_checks'] + down['shared_checks']
        approved, evidence = True, None
        if policy != 'broad':
            comm['payload_bytes'] += len(pack(original))
            approved = (domain(original['vector'], up) if policy == 'weak_upstream'
                        else shared(original['vector'], up))
            comm['status_bytes'] += len(fixture['budgets'])
            if approved and policy in ('attested', 'skip_local', 'weak_upstream'):
                evidence = issue(original, up)
        candidate_decisions = []
        for budget in fixture['budgets']:
            if not approved:
                decision = False
            else:
                if current is not None:
                    exposure += 1
                    comm['payload_bytes'] += len(pack(current))
                if evidence is not None:
                    comm['evidence_bytes'] += len(pack(evidence))
                if policy in ('broad', 'gate'):
                    decision = (None if current is None or budget is None else
                                shared(current['vector'], down) and local(current['vector'], budget, down))
                else:
                    decision = receive(current, budget, evidence, down, policy == 'skip_local')
            candidate_decisions.append(decision)
        decisions.append(candidate_decisions)
        checks_per_candidate.append(up['shared_checks'] + down['shared_checks'] - before)
    # Scoring boundary: no oracle values exist until every policy decision is done.
    targets = [[oracle(a, b) for b in fixture['budgets']] for a in fixture['current']]
    false_accept_fanout = [sum(d is True and t is False for d, t in zip(ds, ts))
                           for ds, ts in zip(decisions, targets)]
    flat = [x for row in decisions for x in row]
    compute = sum(up[k] + down[k] for k in OP_KEYS)
    byte_cost = sum(up[k] + down[k] for k in BYTE_KEYS) + sum(comm.values())
    return dict(policy=policy, cell=fixture['cell'], decisions=decisions, oracle=targets,
                setup=dict(vectors_materialized=8, integers_materialized=sum(len(a['vector']) for a in fixture['original']),
                           original_serialized_bytes=sum(len(pack(a)) for a in fixture['original']),
                           recipient_contracts=len(fixture['budgets'])),
                assumed_generation_units=sum(len(a['vector']) for a in fixture['original']),
                upstream={k: up[k] for k in COUNTER_KEYS}, downstream={k: down[k] for k in COUNTER_KEYS},
                communication={k: comm[k] for k in ('payload_bytes', 'evidence_bytes', 'status_bytes')},
                shared_checks=sum(checks_per_candidate),
                duplicate_shared_checks=sum(max(0, c - 1) for c in checks_per_candidate),
                checks_per_candidate=checks_per_candidate, exposure=exposure,
                reused=down['reused'], fallbacks=down['fallbacks'],
                accepted=sum(x is True for x in flat), rejected=sum(x is False for x in flat),
                unavailable=sum(x is None for x in flat), false_accept=sum(false_accept_fanout),
                false_accept_fanout=false_accept_fanout,
                false_reject=sum(d is False and t is True for ds, ts in zip(decisions, targets) for d, t in zip(ds, ts)),
                compute_only=compute, total_unit_weight=compute + byte_cost)


def summary(receipt):
    rows = receipt['rows']
    primary = [row for row in rows if row['cell']['fault'] == 'none']
    lines = ['# Staged-release v1 results', '',
             '**LOCAL modeled-cost experiment; TRUSTED ATTESTATION, not a succinct proof of truth.**', '',
             f"{len(receipt['fixtures'])} matched cells; {len(rows)} policy rows; 144 primary cells and 20 fault cells.",
             'Eight candidates per cell; five policies. All fixtures, decisions and counters are in the JSON receipt.', '',
             '## Correctness', '', '| Policy | False accepts | False rejects | Unavailable |', '|---|---:|---:|---:|']
    for p in POLICIES:
        selected = [r for r in rows if r['policy'] == p]
        lines.append(f"| {p} | {sum(r['false_accept'] for r in selected)} | {sum(r['false_reject'] for r in selected)} | {sum(r['unavailable'] for r in selected)} |")
    lines.extend(['', 'All safe-policy decisions match the independent oracle, including every available fault case.',
                  'Unsafe controls are deliberately injected common-validator or local-omission faults, not incident-rate measurements.', '',
                  '## Primary cost wins/ties/losses versus broad', '',
                  '| Policy | Compute wins/ties/losses | Total unit-weight wins/ties/losses |', '|---|---|---|'])
    for p in POLICIES[1:]:
        counts = []
        for metric in ('compute_only', 'total_unit_weight'):
            differences = [r[metric] - next(b[metric] for b in primary if b['policy'] == 'broad' and b['cell'] == r['cell'])
                           for r in primary if r['policy'] == p]
            counts.append('/'.join(str(sum(test(d) for d in differences)) for test in (lambda d: d < 0, lambda d: d == 0, lambda d: d > 0)))
        lines.append(f'| {p} | {counts[0]} | {counts[1]} |')
    lines.extend(['', 'Unsafe controls are not eligible cost winners; their costs are shown only as ablations.', '',
                  '## Representative safe-policy wins AND losses', '',
                  '| N | Size | Validity | Local | Policy | Compute | Total | Exposure | Shared checks |',
                  '|---:|---:|---|---|---|---:|---:|---:|---:|'])
    for n, size, validity, compatibility in [(1, 8, 'all', 'all'), (64, 8, 'all', 'all'),
                                            (64, 32, 'all', 'all'), (64, 32, 'mixed', 'half'),
                                            (64, 32, 'all', 'none')]:
        for p in SAFE:
            r = next(r for r in primary if r['cell'] == dict(n=n, size=size, seed=7, validity=validity, local=compatibility, fault='none') and r['policy'] == p)
            lines.append(f"| {n} | {size} | {validity} | {compatibility} | {p} | {r['compute_only']} | {r['total_unit_weight']} | {r['exposure']} | {r['shared_checks']} |")
    lines.extend(['', '## Boundary and accounting', '',
        'Compute-only counts domain/pair/modulo/local/metadata operations and authentication invocations; it excludes per-byte work. Total adds SHA content bytes, HMAC message bytes, and transmitted payload/evidence/status bytes at unit weight. These are uncalibrated mixed-unit sensitivities, not wall-clock speedups.',
        'Receipt counters split setup, upstream, downstream and communication. Materialization/generation assumption is one unit per integer, separate from validation totals and matched across policies. Actual prime-pool generation, RNG, serialization CPU, oracle, provenance/receipt I/O, allocation, network framing/encryption/retries, key provisioning, authoritative context acquisition, energy and labor are excluded. HMAC internal padding/key expansion is not counted per byte.',
        'HMAC uses a public deterministic laboratory key: origin authentication is simulated, not deployed security. Even real secret-key authentication binds an assertion, not its truth. Recipients see the full current artifact, evidence and current local budget; no oracle labels. Stale evidence falls back to independent checking. Shared evidence never covers recipient-local budgets.',
        'Fault metadata is authoritative and visible by assumption; hidden stale dependencies are not solved. Upstream rejects remain sound only because the bounded downstream mutation never repairs a previously invalid artifact. Missing payload/contract is unavailable, tested separately, not claimed equivalent to a complete-data oracle.',
        'This demonstrates conditional amortization and common-mode failure exposure, not P versus NP, mathematical proof compression, external-action authorization, real network performance or incident probabilities.', '',
        '## Reproducibility', '', f"Frozen protocol SHA-256: `{receipt['provenance']['protocol_sha256']}`.",
        'JSON embeds the source hashes and exact imported module path. Runner uses exclusive output creation and reads back both JSON and Markdown. Independent run prefixes have byte-identical content; timestamps and prefix names are intentionally absent.', ''])
    return '\n'.join(lines)
