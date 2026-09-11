"""Queue-migration v3: independently specified burst/on-off workload family."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import deque
from pathlib import Path
from typing import Any, Deque, Dict, Iterable, List, Tuple

STAGES = ("generation", "evaluation", "integration", "maintenance", "retirement")
SEEDS = (11, 12, 13)
HORIZON = 80


# This module intentionally does not import the v2 simulator. The workload and
# queue traversal are independently specified for a cross-instrument check.
def schedule(seed: int, mean_rate: int, horizon: int, family: str) -> List[int]:
    if family == "burst_train":
        # Five ticks on at twice the mean, five ticks off: same long-run mean.
        return [2 * mean_rate if (tick // 5) % 2 == 0 else 0 for tick in range(horizon)]
    if family == "jittered":
        rng = random.Random(seed)
        return [mean_rate + (1 if rng.random() < 0.5 else -1) if mean_rate > 1 else mean_rate for _ in range(horizon)]
    raise ValueError(f"unknown workload family: {family}")


def conditions() -> List[Dict[str, Any]]:
    rows = [
        {"name": f"generation_sweep_r{r}", "family": "generation_sweep", "rate": r, "caps": (r, 4, 4, 4, 4)}
        for r in (1, 2, 4, 8)
    ]
    for stage, caps in {
        "evaluation": (4, 1, 4, 4, 4),
        "integration": (4, 4, 1, 4, 4),
        "maintenance": (4, 4, 4, 1, 4),
        "retirement": (4, 4, 4, 4, 1),
    }.items():
        rows.append({"name": f"capacity_ladder_{stage}", "family": "capacity_ladder", "rate": 4, "caps": caps})
    return rows


def simulate(seed: int, condition: Dict[str, Any], workload: str, horizon: int = HORIZON) -> Dict[str, Any]:
    arrivals = schedule(seed, condition["rate"], horizon, workload)
    queues: List[Deque[Tuple[int, int]]] = [deque() for _ in STAGES]
    entered = [0] * len(STAGES)
    exited = [0] * len(STAGES)
    maximum = [0] * len(STAGES)
    queue_area = [0] * len(STAGES)
    wait_total = [0] * len(STAGES)
    completed = 0
    next_id = 0
    final_tick = horizon + horizon * sum(condition["caps"]) + 100

    for tick in range(final_tick):
        if tick < horizon:
            for _ in range(arrivals[tick]):
                queues[0].append((next_id, tick))
                entered[0] += 1
                next_id += 1
        for idx, cap in enumerate(condition["caps"]):
            moved = min(cap, len(queues[idx]))
            for _ in range(moved):
                item_id, entered_tick = queues[idx].popleft()
                exited[idx] += 1
                wait_total[idx] += tick - entered_tick + 1
                if idx + 1 < len(STAGES):
                    queues[idx + 1].append((item_id, tick))
                    entered[idx + 1] += 1
                else:
                    completed += 1
        for idx, queue in enumerate(queues):
            maximum[idx] = max(maximum[idx], len(queue))
            queue_area[idx] += len(queue)
        if tick >= horizon and not any(queues):
            break
    else:
        raise AssertionError("workload did not drain within finite bound")

    total_ticks = tick + 1
    rows = []
    for idx, stage in enumerate(STAGES):
        rows.append({
            "stage": stage,
            "capacity": condition["caps"][idx],
            "entered": entered[idx],
            "exited": exited[idx],
            "max_queue": maximum[idx],
            "average_queue": round(queue_area[idx] / total_ticks, 6),
            "throughput": round(exited[idx] / total_ticks, 6),
            "utilization": round(exited[idx] / (condition["caps"][idx] * total_ticks), 6),
            "mean_wait": round(wait_total[idx] / exited[idx], 6) if exited[idx] else 0.0,
            "final_queue": len(queues[idx]),
        })
    bottleneck = max(range(len(STAGES)), key=lambda idx: (maximum[idx], -idx))
    return {
        "seed": seed,
        "workload_family": workload,
        "condition": condition["name"],
        "condition_family": condition["family"],
        "mean_rate": condition["rate"],
        "capacities": dict(zip(STAGES, condition["caps"])),
        "arrival_total": sum(arrivals),
        "generated": next_id,
        "completed": completed,
        "drained": not any(queues),
        "ticks_executed": total_ticks,
        "bottleneck": STAGES[bottleneck],
        "stages": rows,
    }


def audit(row: Dict[str, Any]) -> None:
    assert row["arrival_total"] == row["generated"] == row["completed"]
    assert row["drained"] is True
    stages = row["stages"]
    assert stages[0]["entered"] == row["generated"]
    for left, right in zip(stages, stages[1:]):
        assert left["exited"] == right["entered"]
        assert left["final_queue"] == 0
    assert stages[-1]["exited"] == row["completed"]


def run(horizon: int = HORIZON) -> Dict[str, Any]:
    records = [
        simulate(seed, condition, workload, horizon)
        for workload in ("burst_train", "jittered")
        for condition in conditions()
        for seed in SEEDS
    ]
    for row in records:
        audit(row)
    payload: Dict[str, Any] = {
        "protocol_id": "queue-migration-v3",
        "status": "synthetic_fixture",
        "workloads": ["burst_train", "jittered"],
        "seeds": list(SEEDS),
        "horizon": horizon,
        "stages": list(STAGES),
        "records": records,
        "independent_audit": "passed",
        "falsifiers": [
            "flow conservation fails in either workload family",
            "the release ladder fails to localize the constrained stage",
            "the generation sweep fails to expose evaluation under high burst load",
            "a condition fails to drain within its finite bound",
        ],
        "interpretation_boundary": (
            "Independent synthetic workload-family cross-check only; no field, deployment, "
            "stationarity, or universal queueing claim."
        ),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["input_sha256"] = hashlib.sha256(canonical).hexdigest()
    return payload


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
    lines = [
        "# Queue migration v3 independent workload cross-check",
        "",
        f"status: {receipt['status']}",
        f"protocol: {receipt['protocol_id']}",
        f"records: {len(receipt['records'])}",
        f"independent_audit: {receipt['independent_audit']}",
        f"input_sha256: {receipt['input_sha256']}",
        "",
        "| workload | condition | bottleneck counts |",
        "|---|---|---|",
    ]
    for workload in receipt["workloads"]:
        for condition in conditions():
            rows = [r for r in receipt["records"] if r["workload_family"] == workload and r["condition"] == condition["name"]]
            counts: Dict[str, int] = {}
            for row in rows:
                counts[row["bottleneck"]] = counts.get(row["bottleneck"], 0) + 1
            lines.append(f"| {workload} | {condition['name']} | {counts} |")
    lines += ["", "Boundary: independent synthetic workload cross-check only."]
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
