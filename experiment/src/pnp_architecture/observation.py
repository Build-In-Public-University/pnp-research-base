"""Executed bounded observation policies. Oracle and source never enter Consumer.

Logical counter units are frozen in docs/protocol-observation-v1.md. Payloads
are integer fields, not bytes; receipt copying and instrumentation are excluded.
"""
from collections import Counter
import hashlib
import json
import random

POLICIES = ('event_log', 'full_snapshot', 'poll_unchecked', 'poll_guarded')
COUNTERS = ('source_write source_sequence source_log_field source_checkpoint_field '
            'source_snapshot_field producer_publish_field delivery_field receive_field '
            'snapshot_compare cache_write calculation_square calculation_total_write '
            'sequence_check schedule_check interval_coordinate contract_check output_field').split()
PAYLOADS = ('sent_fields delivered_fields dropped_fields sent_messages '
            'delivered_messages dropped_messages').split()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True) + '\n'


def make_world(n, changes, seed):
    rng = random.Random(seed)
    state = [rng.randint(-4, 4) for _ in range(n)]
    states, updates = [state.copy()], [[]]
    for _ in range(1, 16):
        step = []
        for i in sorted(rng.sample(range(n), changes)):
            delta = rng.choice((-1, 1))
            value = state[i] + delta
            if not -8 <= value <= 8:
                value = state[i] - delta
            state[i] = value
            step.append([i, value])
        updates.append(step)
        states.append(state.copy())
    return {'n': n, 'changes': changes, 'seed': seed, 'states': states, 'updates': updates}


class Transport:
    """Explicit field publication, transport, and receiver ingestion loops."""
    def __init__(self, counters, payload):
        self.c = counters
        self.p = payload

    def send(self, record, dropped=False):
        wire = []
        for field in record:
            wire.append(field)
            self.c['producer_publish_field'] += 1
            self.p['sent_fields'] += 1
        self.p['sent_messages'] += 1
        routed = []
        for field in wire:
            self.c['delivery_field'] += 1
            if dropped:
                self.p['dropped_fields'] += 1
            else:
                routed.append(field)
                self.p['delivered_fields'] += 1
        self.p['dropped_messages' if dropped else 'delivered_messages'] += 1
        if dropped:
            return None
        received = []
        for field in routed:
            received.append(field)
            self.c['receive_field'] += 1
        return received


class Source:
    """Source writes and logging are co-located, atomic logical transactions."""
    def __init__(self, initial, logging):
        self.state = list(initial)  # fixture initialization outside measured ticks
        self.logging = logging
        self.seq = 0
        self.log = []

    def advance(self, updates, c):
        for index, value in updates:
            self.state[index] = value
            c['source_write'] += 1
            if self.logging:
                self.seq += 1
                c['source_sequence'] += 1
                record = []
                for field in (self.seq, index, value):
                    record.append(field)
                    c['source_log_field'] += 1
                self.log.append(record)

    def feed(self, tick, mode, transport, c):
        events = []
        for record in self.log:
            received = transport.send(record, dropped=mode == 'dropped' and record[0] % 5 == 0)
            if received is not None:
                events.append(received)
        checkpoint = []
        for field in (tick, self.seq):
            checkpoint.append(field)
            c['source_checkpoint_field'] += 1
        return events, transport.send(checkpoint)

    def snapshot(self, tick, transport, c):
        record = []
        for field in (tick, self.seq):
            record.append(field)
            c['source_snapshot_field'] += 1
        for value in self.state:
            record.append(value)
            c['source_snapshot_field'] += 1
        return transport.send(record)


def bound_decision(cache, age, contract, threshold, c):
    """Only observation-relative bounds; never reads a source or true trajectory."""
    intervals = []
    singleton = True
    low_sum = high_sum = 0
    if contract == 'threshold':
        c['calculation_total_write'] += 2
    for value in cache:
        low, high = max(-8, value-age), min(8, value+age)
        intervals.append([low, high])
        c['interval_coordinate'] += 1
        if low != high:
            singleton = False
        if contract == 'threshold':
            nearest = 0 if low <= 0 <= high else min(abs(low), abs(high))
            furthest = max(abs(low), abs(high))
            minimum = nearest * nearest
            c['calculation_square'] += 1
            maximum = furthest * furthest
            c['calculation_square'] += 1
            low_sum += minimum
            c['calculation_total_write'] += 1
            high_sum += maximum
            c['calculation_total_write'] += 1
    proof = {'intervals': intervals}
    if contract == 'exact':
        return (cache if singleton else None), singleton, proof
    proof['sum_square_bounds'] = [low_sum, high_sum]
    c['contract_check'] += 1
    if low_sum >= threshold:
        return True, True, proof
    c['contract_check'] += 1
    if high_sum < threshold:
        return False, True, proof
    return None, False, proof


class Consumer:
    """Observation-only policy. Snapshot acquisition is an explicit paid capability."""
    def __init__(self, n, policy, contract, threshold):
        self.cache = [None] * n
        self.policy, self.contract, self.threshold = policy, contract, threshold
        self.total = None
        self.seq = 0
        self.fresh_tick = None

    def replace(self, index, value, c):
        old = self.cache[index]
        if self.contract == 'threshold':
            if self.total is None:
                self.total = 0
                c['calculation_total_write'] += 1
            new_square = value * value
            c['calculation_square'] += 1
            if old is None:
                self.total += new_square
            else:
                old_square = old * old
                c['calculation_square'] += 1
                # One fused accumulator mutation, as prospectively declared.
                self.total = self.total - old_square + new_square
            c['calculation_total_write'] += 1
        self.cache[index] = value
        c['cache_write'] += 1

    def read_snapshot(self, tick, acquire, c):
        record = acquire()
        c['sequence_check'] += 1
        if record[0] != tick:
            raise ValueError('Snapshot is not fresh')
        for index, value in enumerate(record[2:]):
            c['snapshot_compare'] += 1
            if self.cache[index] != value:
                self.replace(index, value, c)
        self.seq, self.fresh_tick = record[1], tick

    def step(self, tick, events, checkpoint, acquire, c):
        recovered = False
        proof = {}
        if self.policy.startswith('poll_'):
            c['schedule_check'] += 1
        if self.fresh_tick is None:
            self.read_snapshot(tick, acquire, c)
            # Initial log checkpoint was published and still must be checked.
            if self.policy == 'event_log':
                c['sequence_check'] += 1
                sequence_ok = checkpoint[1] == self.seq
                c['sequence_check'] += 1
                tick_ok = checkpoint[0] == tick
                if not (sequence_ok and tick_ok):
                    raise ValueError('Initial checkpoint mismatch')
        elif self.policy == 'event_log':
            gap = False
            for sequence, index, value in events:
                c['sequence_check'] += 1
                if sequence != self.seq + 1:
                    gap = True
                # Apply authentic delivered values, even after detecting a gap;
                # no output is emitted until the gap is recovered.
                self.replace(index, value, c)
                self.seq = sequence
            c['sequence_check'] += 1
            sequence_ok = checkpoint[1] == self.seq
            c['sequence_check'] += 1
            tick_ok = checkpoint[0] == tick
            if gap or not sequence_ok or not tick_ok:
                self.read_snapshot(tick, acquire, c)
                recovered = True
            else:
                self.fresh_tick = tick
        elif self.policy == 'full_snapshot' or tick % 4 == 0:
            self.read_snapshot(tick, acquire, c)
        age = tick - self.fresh_tick
        guaranteed = age == 0
        if age and self.policy == 'poll_guarded':
            answer, guaranteed, proof = bound_decision(self.cache, age, self.contract, self.threshold, c)
        elif self.contract == 'exact':
            answer = self.cache
        else:
            c['contract_check'] += 1
            answer = self.total >= self.threshold
        if answer is None:
            output = None
        elif self.contract == 'exact':
            output = []
            for value in answer:
                output.append(value)
                c['output_field'] += 1
        else:
            output = answer
            c['output_field'] += 1
        return {'output': output, 'guaranteed': guaranteed, 'recovered': recovered,
                'cache': self.cache.copy(), 'cached_total': self.total,
                'age': age, 'proof': proof}


def evaluate(output, state, contract, threshold, cache, age):
    """Independent oracle and evidence audit, run only after consumer returns.

    Enumerate each coordinate's tiny admissible domain rather than invoking the
    policy's interval formula. Evaluation never supplies a decision to Consumer.
    """
    truth = list(state) if contract == 'exact' else sum(value ** 2 for value in state) >= threshold
    domains = [[v for v in range(-8, 9) if abs(v - observed) <= age] for observed in cache]
    if contract == 'exact':
        sufficient = all(len(domain) == 1 for domain in domains)
    else:
        minimum = sum(min(v**2 for v in domain) for domain in domains)
        maximum = sum(max(v**2 for v in domain) for domain in domains)
        sufficient = (minimum >= threshold) == (maximum >= threshold)
    return {'truth': truth, 'wrong': output is not None and output != truth,
            'evidence_sufficient': sufficient}


def run_policy(world, policy, contract, transport, threshold=None):
    n = len(world['states'][0])
    threshold = n * 16 if threshold is None else threshold
    source = Source(world['states'][0], policy == 'event_log')
    consumer = Consumer(n, policy, contract, threshold)
    ticks = []
    total_c, total_p = Counter({k: 0 for k in COUNTERS}), Counter({k: 0 for k in PAYLOADS})
    log_peak = 0
    for tick, updates in enumerate(world['updates']):
        c = Counter({k: 0 for k in COUNTERS})
        p = Counter({k: 0 for k in PAYLOADS})
        channel = Transport(c, p)
        source.advance(updates, c)
        log_peak = max(log_peak, sum(len(event) for event in source.log))
        observed = {'events': [], 'checkpoint': None, 'snapshots': []}
        if policy == 'event_log':
            observed['events'], observed['checkpoint'] = source.feed(tick, transport, channel, c)

        def acquire():
            record = source.snapshot(tick, channel, c)
            observed['snapshots'].append(record.copy())  # audit work excluded
            return record

        decision = consumer.step(tick, observed['events'], observed['checkpoint'], acquire, c)
        decision.update(evaluate(decision['output'], world['states'][tick], contract, threshold,
                                 decision['cache'], decision['age']))
        decision.update({'tick': tick, 'observed': observed, 'counters': dict(c), 'payload': dict(p)})
        ticks.append(decision)
        total_c.update(c)
        total_p.update(p)
        source.log.clear()  # bounded synchronous log lifetime
    emitted = sum(t['output'] is not None for t in ticks)
    guaranteed = sum(t['output'] is not None and t['guaranteed'] for t in ticks)
    return {'ticks': ticks, 'counters': dict(total_c), 'payload': dict(total_p),
            'operations': sum(total_c.values()), 'emitted': emitted,
            'unavailable': len(ticks)-emitted, 'guaranteed_emitted': guaranteed,
            'wrong_emitted': sum(t['wrong'] for t in ticks),
            'correct_not_guaranteed': sum(t['output'] is not None and not t['wrong'] and not t['guaranteed'] for t in ticks),
            'correct_insufficient_evidence': sum(t['output'] is not None and not t['wrong'] and not t['evidence_sufficient'] for t in ticks),
            'correct_sufficient_but_uncertified': sum(t['output'] is not None and not t['wrong'] and t['evidence_sufficient'] and not t['guaranteed'] for t in ticks),
            'recoveries': sum(t['recovered'] for t in ticks),
            'retained_log_peak_fields': log_peak, 'cached_vector_entries': n}


def experiment():
    worlds, cells = [], []
    for n in (16, 64):
        for changes in (0, 1, n//4, n):
            for seed in (1, 7, 19):
                world = make_world(n, changes, seed)
                world_id = hashlib.sha256(canonical(world).encode()).hexdigest()
                worlds.append({'id': world_id, **world})
                for transport in ('complete', 'dropped'):
                    for contract in ('exact', 'threshold'):
                        policies = {name: run_policy(world, name, contract, transport) for name in POLICIES}
                        eligible = {name: p['operations'] for name, p in policies.items()
                                    if p['guaranteed_emitted'] == 16 and p['wrong_emitted'] == 0}
                        minimum = min(eligible.values())
                        cells.append({'world_id': world_id, 'n': n, 'changes': changes, 'seed': seed,
                                      'transport': transport, 'contract': contract, 'threshold': 16*n,
                                      'policies': policies,
                                      'full_service_guaranteed_winners': [name for name, cost in eligible.items() if cost == minimum]})
    return {'schema': 'observation-v1', 'worlds': worlds, 'cells': cells,
            'cost_model': 'unit sum of declared executed logical counters; not time or energy',
            'counter_names': COUNTERS, 'payload_names': PAYLOADS}
