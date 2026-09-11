"""Deterministic queue-migration fixture for causal-compression research.

This instrument separates two questions:
1. generation sweep: does extra upstream load expose the first downstream
   bottleneck when downstream capacities are held fixed?
2. capacity-release ladder: when the active bottleneck is released, does the
   bottleneck move to the next constrained lifecycle stage?

It is a synthetic instrumentation fixture, not evidence about deployed
organizations, AI systems, or universal queueing laws.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Deque, Dict, Iterable, List, Tuple

STAGES = ("generation", "evaluation", "integration", "maintenance", "retirement")


@dataclass(frozen=True)
class Condition:
    name: str
    capacities: Tuple[int, int, int, int, int]
    family: str
    generation_rate: int


def _simulate(condition: Condition, horizon: int = 40) -> Dict[str, Any]:
    if horizon <= 0 or any(c <= 0 for c in condition.capacities):
        raise ValueError("horizon and capacities must be positive")
    queues: List[Deque[Tuple[int, int]]] = [deque() for _ in STAGES]
    queue_sum = [0] * len(STAGES)
    max_queue = [0] * len(STAGES)
    completed: List[int] = []
    stage_wait = [0] * len(STAGES)
    next_id = 0
    tick = -1

    # Drain enough ticks for this finite fixture. If the pipeline is unstable,
    # the explicit upper bound is recorded rather than hiding the condition.
    ticks = horizon + horizon * sum(condition.capacities) + 20
    for tick in range(ticks):
        if tick < horizon:
            arrivals = condition.capacities[0]
            for _ in range(arrivals):
                queues[0].append((next_id, tick))
                next_id += 1
        for idx in range(len(STAGES)):
            for _ in range(min(condition.capacities[idx], len(queues[idx]))):
                item_id, entered = queues[idx].popleft()
                stage_wait[idx] += tick - entered + 1
                if idx + 1 < len(STAGES):
                    queues[idx + 1].append((item_id, tick))
                else:
                    completed.append(item_id)
        for idx, queue in enumerate(queues):
            queue_sum[idx] += len(queue)
            max_queue[idx] = max(max_queue[idx], len(queue))
        if tick >= horizon and not any(queues):
            break

    total = next_id
    drained = len(completed) == total
    backlog = [len(q) for q in queues]
    avg_queue = [round(value / (tick + 1), 6) for value in queue_sum]
    stage_metrics = []
    for idx, stage in enumerate(STAGES):
        capacity = condition.capacities[idx]
        demand = total if idx == 0 else total
        stage_metrics.append({
            "stage": stage,
            "capacity_per_tick": capacity,
            "max_queue": max_queue[idx],
            "final_queue": backlog[idx],
            "average_queue": avg_queue[idx],
            "utilization_over_active_ticks": round(
                min(1.0, demand / (capacity * max(1, tick + 1))), 6
            ),
            "cumulative_wait_ticks": stage_wait[idx],
        })
    # The active bottleneck is the stage with the greatest queue burden,
    # breaking ties by lifecycle order for deterministic interpretation.
    bottleneck = max(
        range(len(STAGES)), key=lambda i: (max_queue[i], -i)
    )
    return {
        "condition": condition.name,
        "family": condition.family,
        "generation_rate": condition.generation_rate,
        "capacities": dict(zip(STAGES, condition.capacities)),
        "horizon": horizon,
        "generated": total,
        "completed": len(completed),
        "drained": drained,
        "ticks_executed": tick + 1,
        "bottleneck_by_max_queue": STAGES[bottleneck],
        "stages": stage_metrics,
    }


def build_conditions() -> List[Condition]:
    conditions: List[Condition] = []
    # Upstream sweep: all downstream capacities fixed. This is deliberately
    # capable of producing a negative result: evaluation may remain the first
    # constrained stage rather than migrating further downstream.
    for rate in (1, 2, 4, 8):
        conditions.append(Condition(
            name=f"generation_sweep_r{rate}",
            capacities=(rate, 4, 4, 4, 4),
            family="generation_sweep_fixed_downstream",
            generation_rate=rate,
        ))
    # Release one bottleneck at a time to test migration through the lifecycle.
    ladder = {
        "evaluation": (4, 1, 4, 4, 4),
        "integration": (4, 4, 1, 4, 4),
        "maintenance": (4, 4, 4, 1, 4),
        "retirement": (4, 4, 4, 4, 1),
    }
    for stage, capacities in ladder.items():
        conditions.append(Condition(
            name=f"capacity_ladder_{stage}",
            capacities=capacities,
            family="capacity_release_ladder",
            generation_rate=4,
        ))
    return conditions


def run(horizon: int = 40) -> Dict[str, Any]:
    records: List[Dict[str, Any]] = [_simulate(condition, horizon=horizon) for condition in build_conditions()]
    payload = {
        "protocol_id": "queue-migration-v1",
        "status": "synthetic_fixture",
        "seed": 0,
        "stages": list(STAGES),
        "horizon": horizon,
        "conditions": records,
        "falsifiers": [
            "generation pressure does not appear at a downstream stage when its capacity is exceeded",
            "releasing an active bottleneck does not move the maximum queue burden to another stage",
            "the result depends on unordered iteration or changes across identical runs",
            "a condition fails to drain but is reported as a completed lifecycle",
        ],
        "interpretation_boundary": (
            "Synthetic fixture for queue accounting and bottleneck localization only; "
            "not evidence for deployed organizational, AI, market, or universal queueing claims."
        ),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["input_sha256"] = hashlib.sha256(canonical).hexdigest()
    return payload


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--horizon", type=int, default=40)
    args = parser.parse_args(list(argv) if argv is not None else None)
    receipt = run(args.horizon)
    output = Path(args.output)
    summary = Path(args.summary)
    if output.exists() or summary.exists():
        raise SystemExit("refusing to overwrite an existing artifact")
    output.parent.mkdir(parents=True, exist_ok=True)
    summary.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Queue migration v1 synthetic fixture",
        "",
        f"status: {receipt['status']}",
        f"protocol: {receipt['protocol_id']}",
        f"input_sha256: {receipt['input_sha256']}",
        "",
        "| condition | family | generated | completed | drained | bottleneck | max queues |",
        "|---|---|---:|---:|---|---|---|",
    ]
    for record in receipt["conditions"]:
        maxima = ", ".join(
            f"{stage}={next(x['max_queue'] for x in record['stages'] if x['stage'] == stage)}"
            for stage in STAGES
        )
        lines.append(
            f"| {record['condition']} | {record['family']} | {record['generated']} | "
            f"{record['completed']} | {record['drained']} | {record['bottleneck_by_max_queue']} | {maxima} |"
        )
    lines += ["", "Boundary: synthetic instrumentation only; no deployment or general-law claim."]
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
