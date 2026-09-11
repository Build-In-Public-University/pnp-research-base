# Queue migration v4 protocol

Status: frozen trace-derived calibration
Protocol ID: `queue-migration-v4`
Source: `conversation/records.jsonl`

## Source boundary

This calibration uses one public archive trace. It reads record timestamps and role labels only. Message content is not loaded into the receipt or result summary. The source is anchored by SHA-256:

```text
dffc63dce4c36a12e28f5dce447ca997516a7ea4c099d3a46a5d96262053eb38
```

The manifest records the same digest for the archive's record file. This is one trace, not a sample of participants or deployments.

## Workload construction

Timestamped records are binned into one-minute demand buckets relative to the first record. The replay reports record count, role counts, start/end timestamps, bin width, horizon, maximum demand per bin, and total demand. It does not publish content, IDs, or reconstructed dialogue.

The trace contains 1,190 records across 494 one-minute bins. Demand is replayed as a finite arrival schedule. A generation capacity cap may leave source demand ungenerated; that shortfall is reported rather than silently dropped.

## Conditions

### Generation-capacity sweep

`generation_sweep_cap{1,2,4,8}` applies the trace demand with the named generation cap and downstream capacities fixed at 4. This asks whether a high enough upstream cap exposes evaluation pressure in the trace workload.

### Capacity-release ladder

The trace is replayed with generation capacity 128 and all unconstrained downstream stages at 128. Exactly one of evaluation, integration, maintenance, or retirement is constrained to capacity 4. This asks whether measured queue burden localizes to the deliberately constrained lifecycle stage.

## Outcomes

Every record reports generated, source shortfall, completed, drain status, finite replay duration, bottleneck, and per-stage entered/exited counts, maximum and average queue, throughput, utilization, mean wait, and final queue.

## Independent audit

The separate auditor checks:

```text
trace demand - generated = source shortfall
generated = completed
exit(stage_i) = enter(stage_{i+1})
all final queues = 0
```

## Falsifiers

- source hash differs from the manifest-anchored hash;
- stage flow conservation fails;
- replay fails to drain within its finite bound;
- high generation capacity does not expose downstream evaluation pressure when trace demand exceeds evaluation service;
- the capacity-release ladder fails to localize the deliberately constrained stage;
- message content enters any emitted artifact.

## Interpretation boundary

This is one anonymized archive-trace replay. It supports a narrow calibration statement only. It does not establish stationarity, causality about participants, deployment relevance, organizational behavior, AI-system behavior, or a universal queueing law. The trace is historical and bounded; no extrapolation beyond its observed timestamp sequence is licensed.

## Reproduction

```bash
PYTHONPATH=src python3 -m unittest tests.test_queue_migration_v4_trace -v
PYTHONPATH=src python3 scripts/run_queue_migration_v4_trace.py \
  --source ../conversation/records.jsonl \
  --output artifacts/queue_migration_v4.json \
  --summary artifacts/queue_migration_v4.md
```

The runner verifies the source hash and refuses to overwrite existing artifacts.
