# Queue migration v1 results

Status: `synthetic_fixture`
Protocol: `queue-migration-v1`
Receipt: `artifacts/queue_migration_v1.json`
Input hash: `64e6bf94ef7422c744cf9aebea4928b562952c41383a4aa4be5818fda97321c5`

## Execution

The targeted test suite passed 5/5 tests. The deterministic runner completed with exit code 0. All eight conditions drained completely: generated candidates equaled completed candidates in every condition.

## Observed fixture output

| condition | bottleneck by maximum queue | generated | completed | drained |
|---|---|---:|---:|---|
| generation sweep, rate 1 | generation | 40 | 40 | yes |
| generation sweep, rate 2 | generation | 80 | 80 | yes |
| generation sweep, rate 4 | generation | 160 | 160 | yes |
| generation sweep, rate 8 | evaluation | 320 | 320 | yes |
| release ladder: evaluation | evaluation | 160 | 160 | yes |
| release ladder: integration | integration | 160 | 160 | yes |
| release ladder: maintenance | maintenance | 160 | 160 | yes |
| release ladder: retirement | retirement | 160 | 160 | yes |

## Interpretation

The upstream sweep shows a finite threshold effect: rates 1–4 do not create a queue under the fixed downstream capacities, while rate 8 creates an evaluation queue. The capacity-release ladder localizes the active queue to the deliberately constrained stage, producing the intended lifecycle sequence.

This is an instrument result, not a general queueing result. The fixture uses deterministic integer arrivals, fixed service capacities, a finite horizon, and a finite drain phase. It does not establish that real organizations or AI systems exhibit the same migration pattern, nor does it estimate throughput, welfare, energy, or deployment reliability.

The next empirical step, if warranted, is not to enlarge this fixture rhetorically. It is to add controlled workload variability, finite-mean/stationarity checks, and an independently implemented queue accounting path before making a stronger claim.
