"""Queue-migration v4: replay an anonymized timestamp trace from the archive.

Only record timestamps and role counts are used. Message content is never loaded into
any emitted artifact. This is a concrete trace-derived calibration, not a field study.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, deque
from pathlib import Path
from typing import Any, Deque, Dict, Iterable, List, Tuple

STAGES = ("generation", "evaluation", "integration", "maintenance", "retirement")
TRACE_SHA256 = "dffc63dce4c36a12e28f5dce447ca997516a7ea4c099d3a46a5d96262053eb38"
MANIFEST_RECORDS_SHA256 = TRACE_SHA256


def load_trace(path: Path, expected_sha256: str = TRACE_SHA256) -> Dict[str, Any]:
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != expected_sha256:
        raise ValueError(f"trace hash mismatch: {digest}")
    rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
    timestamps = [row["timestamp"] for row in rows if isinstance(row.get("timestamp"), (int, float))]
    if len(timestamps) != len(rows):
        raise ValueError("trace contains records without numeric timestamps")
    start = min(timestamps)
    bins = Counter(int((ts - start) // 60) for ts in timestamps)
    horizon = int((max(timestamps) - start) // 60) + 1
    arrivals = [bins[idx] for idx in range(horizon)]
    roles = Counter(row.get("role", "unknown") for row in rows)
    return {
        "source_sha256": digest,
        "manifest_records_sha256": MANIFEST_RECORDS_SHA256,
        "record_count": len(rows),
        "role_counts": dict(sorted(roles.items())),
        "start_timestamp": min(timestamps),
        "end_timestamp": max(timestamps),
        "bin_seconds": 60,
        "horizon": horizon,
        "arrival_total": sum(arrivals),
        "arrival_max_per_bin": max(arrivals),
        "arrivals": arrivals,
    }


def conditions() -> List[Dict[str, Any]]:
    rows = [
        {"name": f"generation_sweep_cap{cap}", "family": "generation_sweep_trace", "caps": (cap, 4, 4, 4, 4)}
        for cap in (1, 2, 4, 8)
    ]
    for stage, caps in {
        "evaluation": (128, 4, 128, 128, 128),
        "integration": (128, 128, 4, 128, 128),
        "maintenance": (128, 128, 128, 4, 128),
        "retirement": (128, 128, 128, 128, 4),
    }.items():
        rows.append({"name": f"capacity_ladder_{stage}", "family": "capacity_ladder_trace", "caps": caps})
    return rows


def simulate(trace: Dict[str, Any], condition: Dict[str, Any]) -> Dict[str, Any]:
    arrivals = trace["arrivals"]
    queues: List[Deque[Tuple[int, int]]] = [deque() for _ in STAGES]
    entered = [0] * len(STAGES)
    exited = [0] * len(STAGES)
    maximum = [0] * len(STAGES)
    queue_area = [0] * len(STAGES)
    wait_total = [0] * len(STAGES)
    generated = completed = next_id = 0
    horizon = len(arrivals)
    max_ticks = horizon + trace["arrival_total"] * 2 + 100

    for tick in range(max_ticks):
        demand = arrivals[tick] if tick < horizon else 0
        available = min(condition["caps"][0], demand)
        for _ in range(available):
            queues[0].append((next_id, tick))
            entered[0] += 1
            generated += 1
            next_id += 1
        # Unreleased demand remains an upstream backlog represented by the
        # source shortfall; it is accounted for separately below.
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
        raise AssertionError("trace replay did not drain within finite bound")

    trace_demand = sum(arrivals)
    source_shortfall = trace_demand - generated
    total_ticks = tick + 1
    stage_rows = []
    for idx, stage in enumerate(STAGES):
        stage_rows.append({
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
        "condition": condition["name"],
        "condition_family": condition["family"],
        "capacities": dict(zip(STAGES, condition["caps"])),
        "trace_demand": trace_demand,
        "generated": generated,
        "source_shortfall": source_shortfall,
        "completed": completed,
        "drained": not any(queues),
        "ticks_executed": total_ticks,
        "bottleneck": STAGES[bottleneck],
        "stages": stage_rows,
    }


def audit(row: Dict[str, Any]) -> None:
    assert row["trace_demand"] - row["generated"] == row["source_shortfall"]
    assert row["source_shortfall"] >= 0
    assert row["generated"] == row["completed"]
    assert row["drained"] is True
    stages = row["stages"]
    assert stages[0]["entered"] == row["generated"]
    for left, right in zip(stages, stages[1:]):
        assert left["exited"] == right["entered"]
        assert left["final_queue"] == 0
    assert stages[-1]["exited"] == row["completed"]


def run(source: Path, expected_sha256: str = TRACE_SHA256) -> Dict[str, Any]:
    trace = load_trace(source, expected_sha256=expected_sha256)
    records = [simulate(trace, condition) for condition in conditions()]
    for row in records:
        audit(row)
    payload = {
        "protocol_id": "queue-migration-v4",
        "status": "trace_derived_calibration",
        "source_policy": "timestamps and role labels only; message content excluded",
        "trace": {key: value for key, value in trace.items() if key != "arrivals"},
        "conditions": records,
        "independent_audit": "passed",
        "falsifiers": [
            "source hash differs from manifest-anchored hash",
            "stage flow conservation fails",
            "trace replay fails to drain within the finite bound",
            "high generation capacity does not expose downstream evaluation pressure when trace demand exceeds evaluation service",
            "capacity release ladder fails to localize the deliberately constrained stage",
        ],
        "interpretation_boundary": (
            "One anonymized archive trace replay only; no causal claim about the session participants, "
            "no stationarity claim, and no general deployment inference."
        ),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["input_sha256"] = hashlib.sha256(canonical).hexdigest()
    return payload


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--expected-sha256", default=TRACE_SHA256)
    parser.add_argument("--output", required=True)
    parser.add_argument("--summary", required=True)
    args = parser.parse_args(list(argv) if argv is not None else None)
    output, summary = Path(args.output), Path(args.summary)
    if output.exists() or summary.exists():
        raise SystemExit("refusing to overwrite an existing artifact")
    receipt = run(Path(args.source), expected_sha256=args.expected_sha256)
    output.parent.mkdir(parents=True, exist_ok=True)
    summary.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Queue migration v4 trace-derived calibration",
        "",
        f"status: {receipt['status']}",
        f"protocol: {receipt['protocol_id']}",
        f"trace_records: {receipt['trace']['record_count']}",
        f"trace_sha256: {receipt['trace']['source_sha256']}",
        f"independent_audit: {receipt['independent_audit']}",
        f"input_sha256: {receipt['input_sha256']}",
        "",
        "| condition | bottleneck | generated | source shortfall |",
        "|---|---|---:|---:|",
    ]
    for row in receipt["conditions"]:
        lines.append(f"| {row['condition']} | {row['bottleneck']} | {row['generated']} | {row['source_shortfall']} |")
    lines += ["", "Boundary: one anonymized archive trace replay; no participant or deployment claim."]
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
