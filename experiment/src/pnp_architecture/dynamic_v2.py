"""Consequence-aware certificate timing built on the frozen dynamic v1 engine."""
from collections import Counter
from copy import deepcopy

from pnp_architecture.dynamic import DynamicEngine, make_trajectory, oracle

POLICIES = ("selective_repair", "certificate_repair", "delayed_certificate", "unchecked_cache")
CONSEQUENCE_PENALTIES = (0, 10, 100, 1000, 10000)


def _failure(seed, t, output_index, rate):
    if rate <= 0:
        return False
    if rate >= 1:
        return True
    return ((seed + 17 * t + output_index) % 100) < int(rate * 100)


def _event_for_policy(event, engine, policy, t, cert_interval):
    if policy != "delayed_certificate" or t % cert_interval == 0:
        return event, True
    delayed = deepcopy(event)
    delayed["certificate_digest"] = engine.certificate_digest
    delayed["actual_dependencies"] = list(delayed["visible_dependencies"])
    return delayed, False


def run_consequence_cell(n, state_changes, seed, cert_interval=3, hidden_drift=True,
                         graph_changes=None, stale_failure_rate=0.25,
                         downstream_penalty=100):
    if cert_interval < 1:
        raise ValueError("cert_interval must be positive")
    if not 0 <= stale_failure_rate <= 1:
        raise ValueError("stale_failure_rate must be between 0 and 1")
    world = make_trajectory(n, state_changes, seed, hidden_drift, graph_changes)
    if hidden_drift:
        visible = [tuple(dep) for dep in world[0]["visible_dependencies"]]
        for event in world:
            event["visible_dependencies"] = list(visible)
            event["visible_version"] = 0
    policies = {}
    for policy in POLICIES:
        engine_policy = "certificate_repair" if policy == "delayed_certificate" else policy
        engine = DynamicEngine(engine_policy, world[0])
        totals = Counter(engine.initial_counters)
        rows = [{"t": 0, "certificate_available": True,
                 "returned": deepcopy(engine.result), "wrong_output": False,
                 "stale_failures": 0, "counters": dict(engine.initial_counters)}]
        stale_failures = 0
        unsafe_reuse = 0
        unavailable = 0
        for t, event in enumerate(world[1:], 1):
            supplied, available = _event_for_policy(event, engine, policy, t, cert_interval)
            if not available:
                unavailable += 1
            counters = engine.update(supplied)
            truth = oracle(event["state"], event["actual_dependencies"])
            returned = {"values": list(engine.result["values"]),
                        "total": engine.result["total"], "accepted": engine.result["accepted"]}
            mismatches = [i for i, (a, b) in enumerate(zip(returned["values"], truth["values"])) if a != b]
            wrong = returned != truth
            if wrong and policy != "certificate_repair":
                unsafe_reuse += 1
            row_failures = sum(_failure(seed, t, i, stale_failure_rate) for i in mismatches)
            stale_failures += row_failures
            rows.append({"t": t, "certificate_available": available,
                         "returned": returned, "wrong_output": wrong,
                         "stale_failures": row_failures, "counters": counters})
            totals.update(counters)
        base_operations = sum(totals.values())
        consequence_cost = stale_failures * downstream_penalty
        policies[policy] = {
            "steps": rows,
            "counters": dict(totals),
            "base_operations": base_operations,
            "operations": base_operations,
            "consequence_cost": consequence_cost,
            "total_cost": base_operations + consequence_cost,
            "wrong_outputs": sum(row["wrong_output"] for row in rows),
            "unsafe_reuse": unsafe_reuse,
            "stale_failures": stale_failures,
            "certificate_unavailable": unavailable,
        }
    return {
        "n": n, "state_changes": state_changes, "graph_changes": graph_changes,
        "seed": seed, "hidden_drift": hidden_drift,
        "cert_interval": cert_interval, "stale_failure_rate": stale_failure_rate,
        "downstream_penalty": downstream_penalty, "inputs": world, "policies": policies,
    }


def consequence_surface(receipt, penalties=CONSEQUENCE_PENALTIES):
    rows = []
    for penalty in penalties:
        totals = {}
        for policy, result in receipt["policies"].items():
            totals[policy] = result["base_operations"] + result["stale_failures"] * penalty
        best = min(totals.values())
        rows.append({"penalty": penalty, "totals": totals,
                     "winners": [p for p, value in totals.items() if value == best]})
    return {"penalties": list(penalties), "rows": rows,
            "boundary": "Certificate validation is preferable only when its total modeled cost is lower under the declared synthetic consequence model."}


def experiment():
    cells = []
    for n in (8, 16):
        for state_changes in (0, 1, n // 2, n):
            for graph_changes in (0, n // 2, n):
                for seed in (1, 7, 19):
                    for interval in (1, 3):
                        for hidden in (False, True):
                            cell = run_consequence_cell(n, state_changes, seed, interval, hidden, graph_changes)
                            cell["surface"] = consequence_surface(cell)
                            cells.append(cell)
    return {"status": "executed_dynamic_dependency_consequence_unit_cost_proxy",
            "cells": cells, "policies": POLICIES,
            "consequence_boundary": "Stale failures and downstream penalties are deterministic synthetic consequences, not empirical probabilities or application losses."}
