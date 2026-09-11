# Queue migration v3 protocol

Status: frozen synthetic cross-check
Protocol ID: `queue-migration-v3`

V3 independently specifies both the workload family and queue traversal rather than importing the v2 simulator. It tests whether the v2 bottleneck pattern survives a different implementation.

## Workloads

- `burst_train`: five ticks at twice the declared mean rate, followed by five ticks at zero;
- `jittered`: bounded seeded jitter around the declared mean rate.

Both are finite synthetic workloads. Neither is evidence of a real arrival process.

## Conditions

The v2 conditions are retained:

- generation sweep rates 1, 2, 4, and 8 with downstream capacities fixed at 4;
- capacity-release ladder constraining evaluation, integration, maintenance, or retirement in turn.

Seeds are `11, 12, 13`. The arrival horizon is 80 ticks. Each finite workload must drain completely.

## Independent audit

The v3 auditor checks generated = arrival total = completed, stage-flow conservation, empty final queues, and finite drain completion. It is separate from the simulator's queue update loop.

## Falsifiers

- flow conservation fails in either workload family;
- the release ladder fails to localize the constrained stage;
- the generation sweep fails to expose evaluation under high burst load;
- a condition fails to drain within its finite bound;
- the two independently implemented workload families disagree on the declared mechanism.

## Evidence boundary

A passing v3 cross-check supports only a bounded synthetic instrument statement. It does not establish stationarity, deployment relevance, organizational behavior, AI-system behavior, or a universal queueing law. A trace-derived workload or real operational dataset is a separate evidentiary step.

## Reproduction

```bash
PYTHONPATH=src python3 -m unittest tests.test_queue_migration_v3_bursty -v
PYTHONPATH=src python3 scripts/run_queue_migration_v3_bursty.py \
  --output artifacts/queue_migration_v3.json \
  --summary artifacts/queue_migration_v3.md
```
