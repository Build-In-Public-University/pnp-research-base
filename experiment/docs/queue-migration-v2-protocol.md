# Queue migration v2 protocol

Status: frozen synthetic fixture
Protocol ID: `queue-migration-v2`
Supersedes: none; v1 remains immutable

## Question

When candidate generation becomes cheaper, where does lifecycle pressure accumulate? Does the active bottleneck move downstream when the currently constrained stage is given more capacity?

## Strengthening over v1

V2 adds five deterministic seeds, bounded variable arrivals, observable half-window stationarity diagnostics, per-stage throughput/utilization/time-in-stage, and an independent receipt auditor. The finite-window diagnostic is not a proof of stationarity; it is a gate against silently treating one irregular path as a stationary workload.

## Lifecycle

```text
generation -> evaluation -> integration -> maintenance -> retirement
```

Each stage has integer service capacity per tick. A bounded-jitter arrival schedule is generated from a frozen seed and declared mean rate. Candidates must pass every stage. The finite workload is drained after the arrival horizon; a record is complete only when every queue is empty.

## Conditions

### Generation sweep

`generation_sweep_fixed_downstream_r{1,2,4,8}` varies the declared generation rate while downstream capacities remain 4. This tests whether extra upstream load exposes evaluation as the first constrained downstream stage at high rate.

### Capacity-release ladder

`capacity_ladder_{evaluation,integration,maintenance,retirement}` uses generation capacity 4, gives one named stage capacity 1, and gives all other lifecycle stages capacity 4. This tests localization and downstream movement under controlled release of the active constraint.

## Seeds and schedule

Seeds are `[0, 1, 2, 3, 4]`. For each tick in the 80-tick arrival horizon, arrivals equal the declared integer mean plus one with probability 0.25, using Python's seeded PRNG. The first-half and second-half means are recorded. The diagnostic passes when their difference is no more than `max(1.0, 0.5 * observed_mean)`.

The diagnostic is descriptive only. It does not establish ergodicity, stationarity, or a real workload distribution.

## Primary outcomes

- arrival total and observed arrival mean;
- first/second-half arrival means and finite-window delta;
- generated/completed counts and drain status;
- per-stage entered/exited counts;
- maximum and average queue;
- throughput per tick;
- utilization over the finite run;
- mean time in each stage;
- bottleneck localized by maximum queue with deterministic lifecycle-order tie-breaking.

## Independent audit

The auditor is a separate function from the simulator's queue update loop. It checks:

```text
generated = arrival_total = completed
exit(stage_i) = enter(stage_{i+1})
all final queues = 0
0 <= utilization <= 1
```

A passing audit validates receipt accounting, not the scientific hypothesis.

## Falsifiers

- flow conservation fails under the independent audit;
- a condition does not drain within the declared finite bound;
- the release ladder does not localize the constrained stage;
- the generation sweep does not expose evaluation pressure at rate 8;
- identical seed/condition runs differ;
- finite-window diagnostics are absent or silently treated as proof of stationarity.

## Interpretation boundary

This is a seeded synthetic queue-accounting instrument. It does not establish that real organizations, AI systems, markets, or infrastructures exhibit the same migration pattern. It does not estimate energy, welfare, deployment reliability, or universal queueing laws.

## Reproduction

```bash
PYTHONPATH=src python3 -m unittest tests.test_queue_migration_v2 -v
PYTHONPATH=src python3 scripts/run_queue_migration_v2.py \
  --output artifacts/queue_migration_v2.json \
  --summary artifacts/queue_migration_v2.md
```

The runner refuses to overwrite existing artifacts. The receipt records protocol identity, seeds, falsifiers, independent-audit status, interpretation boundary, and a canonical input hash.
