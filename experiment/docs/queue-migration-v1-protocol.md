# Queue migration v1 protocol

Status: frozen synthetic fixture
Protocol ID: `queue-migration-v1`

## Question

When candidate generation becomes cheaper, where does lifecycle pressure accumulate? Does an active bottleneck move downstream when the currently constrained stage is given more capacity?

## Scope

This is a deterministic queue-accounting instrument. It is not a model-run, field observation, deployment benchmark, or claim about organizations, generative AI, markets, or universal queueing behavior.

## Lifecycle stages

```text
generation -> evaluation -> integration -> maintenance -> retirement
```

Each stage has an integer service capacity per tick. Generation emits candidates for 40 ticks. Each candidate must pass through every stage. The simulator then drains the finite workload. A candidate is complete only after retirement.

## Conditions

1. `generation_sweep_fixed_downstream_r{1,2,4,8}`
   - generation capacity varies;
   - all downstream capacities remain 4;
   - tests whether extra upstream load exposes the first downstream constraint.

2. `capacity_ladder_{evaluation,integration,maintenance,retirement}`
   - generation capacity is 4;
   - exactly one lifecycle stage has capacity 1;
   - all other stages have capacity 4;
   - tests whether the measured maximum queue burden localizes to the constrained stage.

The second family is intentional. An upstream-only sweep cannot prove migration past a permanently saturated first downstream stage. It can only expose that stage. The release ladder is the falsifiable test of downstream movement.

## Primary outcomes

- generated and completed candidate counts;
- drain status;
- maximum queue by stage;
- average queue by stage;
- cumulative wait ticks by stage;
- bottleneck localized as the stage with the largest maximum queue, with lifecycle-order tie-breaking.

## Falsifiers

The fixture fails its intended instrument claim if any of the following occurs:

- generation pressure does not appear at a downstream stage when its capacity is exceeded;
- releasing the active bottleneck does not move the maximum queue burden to the specified constrained stage;
- identical runs differ;
- a condition fails to drain but is reported as complete;
- stage labels, capacities, or denominators are missing from the receipt.

## Interpretation

A passing fixture establishes only that this implementation can represent the declared queue transitions and produce deterministic accounting. It does not establish a general law that real systems migrate bottlenecks in this order. Any paper claim must distinguish the upstream-only result from the capacity-release result.

## Reproduction

From the experiment repository root:

```bash
PYTHONPATH=src python3 -m unittest tests.test_queue_migration_v1 -v
PYTHONPATH=src python3 scripts/run_queue_migration_v1.py \
  --output artifacts/queue_migration_v1-local.json \
  --summary artifacts/queue_migration_v1-local.md
```

The runner refuses to overwrite existing artifacts. The receipt records `status: synthetic_fixture`, protocol identity, falsifiers, interpretation boundary, and a canonical input hash.
