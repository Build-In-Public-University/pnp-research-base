"""Queue-migration v2: seeded variable-arrival synthetic benchmark.

This is a new protocol. queue_migration_v1 remains immutable.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Deque, Dict, Iterable, List, Tuple

STAGES = ("generation", "evaluation", "integration", "maintenance", "retirement")
SEEDS = (0, 1, 2, 3, 4)
HORIZON = 80


@dataclass(frozen=True)
class Condition:
    name: str
    family: str
    mean_generation_rate: int
    capacities: Tuple[int, int, int, int, int]


def build_conditions() -> List[Condition]:
    conditions = [
        Condition(f"generation_sweep_r{r}", "generation_sweep_fixed_downstream", r, (r, 4, 4, 4, 4))
        for r in (1, 2, 4, 8)
    ]
    for stage, capacities in {
        "evaluation": (4, 1, 4, 4, 4),
        "integration": (4, 4, 1, 4, 4),
        "maintenance": (4, 4, 4, 1, 4),
        "retirement": (4, 4, 4, 4, 1),
    }.items():
        conditions.append(Condition(f"capacity_ladder_{stage}", "capacity_release_ladder", 4, capacities))
    return conditions


def arrival_schedule(seed: int, mean_rate: int, horizon: int) -> List[int]:
    """Stationary bounded jitter around a declared mean rate."""
    rng = random.Random(seed)
    return [mean_rate + (1 if rng.random() < 0.25 else 0) for _ in range(horizon)]


def _simulate(seed: int, condition: Condition, horizon: int = HORIZON) -> Dict[str, Any]:
    if horizon <= 1 or any(c <= 0 for c in condition.capacities):
        raise ValueError("horizon must exceed one and capacities must be positive")
    arrivals = arrival_schedule(seed, condition.mean_generation_rate, horizon)
    queues: List[Deque[Tuple[int, int]]] = [deque() for _ in STAGES]
    entered = [0] * len(STAGES)
    exited = [0] * len(STAGES)
    queue_integral = [0] * len(STAGES)
    max_queue = [0] * len(STAGES)
    wait_ticks = [0] * len(STAGES)
    completed = 0
    next_id = 0
    tick = -1
    max_ticks = horizon + horizon * sum(condition.capacities) + 100

    for tick in range(max_ticks):
        if tick < horizon:
            for _ in range(arrivals[tick]):
                queues[0].append((next_id, tick))
                entered[0] += 1
                next_id += 1
        for idx, capacity in enumerate(condition.capacities):
            for _ in range(min(capacity, len(queues[idx]))):
                item_id, entered_tick = queues[idx].popleft()
                exited[idx] += 1
                wait_ticks[idx] += tick - entered_tick + 1
                if idx + 1 < len(STAGES):
                    queues[idx + 1].append((item_id, tick))
                    entered[idx + 1] += 1
                else:
                    completed += 1
        for idx, queue in enumerate(queues):
            queue_integral[idx] += len(queue)
            max_queue[idx] = max(max_queue[idx], len(queue))
        if tick >= horizon and not any(queues):
            break
    else:
        raise AssertionError("finite drain bound exceeded")

    first = arrivals[: horizon // 2]
    second = arrivals[horizon // 2 :]
    first_mean = sum(first) / len(first)
    second_mean = sum(second) / len(second)
    observed_mean = sum(arrivals) / len(arrivals)
    stationarity_delta = abs(first_mean - second_mean)
    # This is a finite-window diagnostic, not a proof of stationarity.
    stationarity_ok = stationarity_delta <= max(1.0, 0.5 * observed_mean)
    ticks_executed = tick + 1
    stage_rows = []
    for idx, stage in enumerate(STAGES):
        stage_rows.append({
            "stage": stage,
            "capacity_per_tick": condition.capacities[idx],
            "entered": entered[idx],
            "exited": exited[idx],
            "max_queue": max_queue[idx],
            "final_queue": len(queues[idx]),
            "average_queue": round(queue_integral[idx] / ticks_executed, 6),
            "throughput_per_tick": round(exited[idx] / ticks_executed, 6),
            "utilization_over_run": round(exited[idx] / (condition.capacities[idx] * ticks_executed), 6),
            "mean_wait_ticks": round(wait_ticks[idx] / exited[idx], 6) if exited[idx] else 0.0,
        })
    bottleneck = max(range(len(STAGES)), key=lambda i: (max_queue[i], -i))
    return {
        "seed": seed,
        "condition": condition.name,
        "family": condition.family,
        "mean_generation_rate": condition.mean_generation_rate,
        "capacities": dict(zip(STAGES, condition.capacities)),
        "horizon": horizon,
        "arrival_total": sum(arrivals),
        "arrival_first_half_mean": round(first_mean, 6),
        "arrival_second_half_mean": round(second_mean, 6),
        "arrival_observed_mean": round(observed_mean, 6),
        "arrival_stationarity_delta": round(stationarity_delta, 6),
        "arrival_stationarity_diagnostic": stationarity_ok,
        "generated": next_id,
        "completed": completed,
        "drained": not any(queues),
        "ticks_executed": ticks_executed,
        "bottleneck_by_max_queue": STAGES[bottleneck],
        "stages": stage_rows,
    }


def audit_record(record: Dict[str, Any]) -> None:
    """Independent conservation audit over emitted counters."""
    stages = record["stages"]
    assert record["generated"] == record["arrival_total"]
    assert record["generated"] == record["completed"]
    assert record["drained"] is True
    assert stages[0]["entered"] == record["generated"]
    for left, right in zip(stages, stages[1:]):
        assert left["exited"] == right["entered"], (left, right)
        assert left["final_queue"] == 0
    assert stages[-1]["exited"] == record["completed"]
    for row in stages:
        assert 0.0 <= row["utilization_over_run"] <= 1.0
        assert row["entered"] >= row["exited"] >= 0


def run(horizon: int = HORIZON) -> Dict[str, Any]:
    records = [_simulate(seed, condition, horizon) for condition in build_conditions() for seed in SEEDS]
    for record in records:
        audit_record(record)
    payload: Dict[str, Any] = {
        "protocol_id": "queue-migration-v2",
        "status": "synthetic_fixture",
        "seeds": list(SEEDS),
        "horizon": horizon,
        "stages": list(STAGES),
        "conditions": records,
        "independent_audit": {
            "status": "passed",
            "checks": [
                "generated equals arrival total and completed total",
                "stage exit equals next-stage entry",
                "all final queues are empty",
                "utilization is bounded in [0,1]",
            ],
        },
        "falsifiers": [
            "flow conservation fails under an independent audit",
            "a condition does not drain within the declared finite bound",
            "the release ladder does not localize the constrained stage",
            "the generation sweep does not expose evaluation pressure at rate 8",
            "identical seed/condition runs differ",
        ],
        "interpretation_boundary": (
            "Seeded synthetic queue accounting only; finite-window stationarity is a diagnostic, "
            "not a proof, and no deployment or universal queueing claim is established."
        ),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["input_sha256"] = hashlib.sha256(canonical).hexdigest()
    return payload


def write_summary(receipt: Dict[str, Any], path: Path) -> None:
    lines = [
        "# Queue migration v2 synthetic fixture",
        "",
        f"status: {receipt['status']}",
        f"protocol: {receipt['protocol_id']}",
        f"seeds: {receipt['seeds']}",
        f"input_sha256: {receipt['input_sha256']}",
        f"independent_audit: {receipt['independent_audit']['status']}",
        "",
        "| condition | seeds | bottleneck counts | stationarity diagnostics |",
        "|---|---:|---|---|",
    ]
    for condition in build_conditions():
        rows = [r for r in receipt["conditions"] if r["condition"] == condition.name]
        counts: Dict[str, int] = {}
        for row in rows:
            counts[row["bottleneck_by_max_queue"]] = counts.get(row["bottleneck_by_max_queue"], 0) + 1
        diagnostics = sum(bool(row["arrival_stationarity_diagnostic"]) for row in rows)
        lines.append(f"| {condition.name} | {len(rows)} | {counts} | {diagnostics}/{len(rows)} pass |")
    lines += ["", "Boundary: synthetic instrumentation only; no deployment or general-law claim."]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--horizon", type=int, default=HORIZON)
    args = parser.parse_args(list(argv) if argv is not None else None)
    output, summary = Path(args.output), Path(args.summary)
    if output.exists() or summary.exists():
        raise SystemExit("refusing to overwrite an existing artifact")
    receipt = run(args.horizon)
    output.parent.mkdir(parents=True, exist_ok=True)
    summary.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    write_summary(receipt, summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
