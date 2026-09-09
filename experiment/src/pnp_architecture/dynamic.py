"""Versioned dependency repair experiment. Counters are synthetic logical units."""
from collections import Counter
import hashlib
import json
import random

POLICIES = (
    "cold_recompute",
    "selective_repair",
    "full_reset",
    "certificate_repair",
    "unchecked_cache",
)


def digest_dependencies(dependencies):
    return hashlib.sha256(json.dumps(dependencies, separators=(",", ":")).encode()).hexdigest()


def base_dependencies(n):
    return [tuple((i + j) % n for j in range(3)) for i in range(n)]


def oracle(state, dependencies):
    values = [sum(state[j] for j in dep) for dep in dependencies]
    total = sum(values)
    return {"values": values, "total": total, "accepted": total <= 2 * len(state)}


def _change_graph(graph, indexes, n):
    graph = [list(dep) for dep in graph]
    for i in indexes:
        candidates = [j for j in range(n) if j not in graph[i]]
        graph[i][-1] = candidates[(i + len(graph[i])) % len(candidates)]
    return [tuple(dep) for dep in graph]


def make_trajectory(n, state_changes, seed, hidden_drift=False, graph_changes=None, steps=8):
    if n < 3 or not 0 <= state_changes <= n:
        raise ValueError("invalid trajectory dimensions")
    if graph_changes is None:
        graph_changes = 1 if state_changes or hidden_drift else 0
    if not 0 <= graph_changes <= n:
        raise ValueError("invalid graph change count")
    rng = random.Random(seed)
    # Varied nonzero baseline makes hidden edge changes observable even with zero state churn.
    state = [(i + 1) * 2 for i in range(n)]
    actual = base_dependencies(n)
    visible = [tuple(dep) for dep in actual]
    version = 0
    out = [{
        "state": list(state),
        "actual_dependencies": [tuple(dep) for dep in actual],
        "visible_dependencies": [tuple(dep) for dep in visible],
        "visible_version": version,
        "certificate_digest": digest_dependencies(actual),
    }]
    for t in range(1, steps + 1):
        changed = sorted(rng.sample(range(n), state_changes)) if state_changes else []
        for j in changed:
            state[j] = (state[j] + 1) % 4
        graph_indexes = sorted(rng.sample(range(n), graph_changes)) if graph_changes else []
        if graph_indexes and (t % 2 == 0 or hidden_drift and t == 1):
            actual = _change_graph(actual, graph_indexes, n)
        hidden = hidden_drift and t == 1
        if not hidden:
            visible = [tuple(dep) for dep in actual]
            if changed or graph_indexes:
                version += 1
        out.append({
            "state": list(state),
            "actual_dependencies": [tuple(dep) for dep in actual],
            "visible_dependencies": [tuple(dep) for dep in visible],
            "visible_version": version,
            "certificate_digest": digest_dependencies(actual),
        })
    return out


class DynamicEngine:
    def __init__(self, policy, first):
        if policy not in POLICIES:
            raise ValueError(policy)
        self.policy = policy
        self.n = len(first["state"])
        self.state = list(first["state"])
        self.dependencies = [tuple(dep) for dep in first["visible_dependencies"]]
        self.certificate_digest = first["certificate_digest"]
        self.result = oracle(self.state, self.dependencies)
        self.stale_acceptances = 0
        self.initial_counters = Counter()
        self._build_index(self.initial_counters)
        self.initial_counters["state_read"] += self.n
        self.initial_counters["output_write"] += self.n
        self.initial_counters["add"] += self.n * 3

    def _build_index(self, counters):
        self.reverse = [[] for _ in range(self.n)]
        counters["graph_construction"] += self.n
        for i, dep in enumerate(self.dependencies):
            counters["dependency_discovery"] += len(dep)
            for j in dep:
                self.reverse[j].append(i)
                counters["index_maintenance"] += 1

    def _affected(self, old_state, new_state, old_deps, new_deps, counters):
        dirty = {i for i, (a, b) in enumerate(zip(old_deps, new_deps)) if a != b}
        counters["dependency_discovery"] += self.n
        changed_inputs = {j for j, (a, b) in enumerate(zip(old_state, new_state)) if a != b}
        counters["state_read"] += self.n
        counters["state_compare"] += self.n
        for j in changed_inputs:
            dirty.update(self.reverse[j])
            counters["index_maintenance"] += len(self.reverse[j])
        return dirty

    def _repair(self, state, dependencies, dirty, counters):
        for i in sorted(dirty):
            counters["output_read"] += 1
            value = 0
            for j in dependencies[i]:
                counters["state_read"] += 1
                counters["add"] += 1
                value += state[j]
            self.result["values"][i] = value
            counters["output_write"] += 1
        if dirty:
            self.result["total"] = sum(self.result["values"])
            counters["output_read"] += self.n
            counters["add"] += self.n
        self.result["accepted"] = self.result["total"] <= 2 * self.n
        counters["output_validation"] += len(dirty)

    def update(self, event):
        counters = Counter(cache_lookup=1)
        new_state = list(event["state"])
        visible = [tuple(dep) for dep in event["visible_dependencies"]]
        actual = [tuple(dep) for dep in event["actual_dependencies"]]
        visible_changed = new_state != self.state or visible != self.dependencies
        actual_changed = new_state != self.state or actual != self.dependencies
        if self.policy == "cold_recompute":
            counters["state_read"] += self.n
            counters["dependency_discovery"] += self.n * 3
            self.result = oracle(new_state, actual)
            counters["output_write"] += self.n
            counters["output_validation"] += self.n
        elif self.policy == "unchecked_cache":
            if actual_changed:
                self.stale_acceptances += 1
                counters["stale_acceptance"] += 1
        elif self.policy == "full_reset":
            if visible_changed:
                counters["graph_construction"] += self.n
                counters["dependency_discovery"] += self.n * 3
                self.dependencies = visible
                self._repair(new_state, visible, set(range(self.n)), counters)
        elif self.policy == "selective_repair":
            if visible_changed:
                dirty = self._affected(self.state, new_state, self.dependencies, visible, counters)
                self.dependencies = visible
                self._build_index(counters)
                self._repair(new_state, visible, dirty, counters)
            elif actual_changed:
                self.stale_acceptances += 1
                counters["stale_acceptance"] += 1
        elif self.policy == "certificate_repair":
            counters["certificate_validation"] += 1
            certificate_changed = event["certificate_digest"] != self.certificate_digest
            if certificate_changed or visible_changed:
                dirty = self._affected(self.state, new_state, self.dependencies, actual, counters)
                self.dependencies = actual
                self.certificate_digest = event["certificate_digest"]
                self._build_index(counters)
                self._repair(new_state, actual, dirty, counters)
        self.state = new_state
        return dict(counters)

    def retained_slots(self):
        return self.n + len(self.dependencies) * 3 + self.n


def run_cell(n, state_changes, seed, hidden_drift=False, graph_changes=None):
    world = make_trajectory(n, state_changes, seed, hidden_drift, graph_changes)
    policies = {}
    for policy in POLICIES:
        engine = DynamicEngine(policy, world[0])
        steps = [{"t": 0, "returned": engine.result.copy(), "counters": dict(engine.initial_counters), "wrong_output": False}]
        totals = Counter(engine.initial_counters)
        for t, event in enumerate(world[1:], 1):
            counters = engine.update(event)
            truth = oracle(event["state"], event["actual_dependencies"])
            returned = {"values": list(engine.result["values"]), "total": engine.result["total"], "accepted": engine.result["accepted"]}
            wrong = returned != truth
            steps.append({"t": t, "returned": returned, "counters": counters, "wrong_output": wrong})
            totals.update(counters)
        policies[policy] = {
            "steps": steps,
            "counters": dict(totals),
            "operations": sum(totals.values()),
            "wrong_outputs": sum(step["wrong_output"] for step in steps),
            "stale_acceptances": engine.stale_acceptances,
            "retained_state_slots": engine.retained_slots(),
        }
    return {
        "n": n,
        "state_changes": state_changes,
        "graph_changes": graph_changes if graph_changes is not None else (1 if state_changes else 0),
        "seed": seed,
        "hidden_drift": hidden_drift,
        "inputs": world,
        "policies": policies,
    }


def experiment():
    cells = [run_cell(n, state_changes, seed, hidden, graph_changes)
             for n in (8, 16)
             for state_changes in (0, 1, n // 2, n)
             for graph_changes in (0, n // 2, n)
             for seed in (1, 7, 19)
             for hidden in (False, True)]
    return {
        "status": "executed_dynamic_dependency_repair_unit_cost_proxy",
        "cells": cells,
        "policies": POLICIES,
        "counter_boundary": "Listed metadata, state, index, certificate, output and arithmetic counters. World generation, oracle, serialization and validation-channel production excluded.",
        "claim_boundary": "Finite synthetic dependency system; no runtime, energy, deployment or P/NP claim.",
    }
