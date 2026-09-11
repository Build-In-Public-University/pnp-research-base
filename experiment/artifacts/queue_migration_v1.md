# Queue migration v1 synthetic fixture

status: synthetic_fixture
protocol: queue-migration-v1
input_sha256: 64e6bf94ef7422c744cf9aebea4928b562952c41383a4aa4be5818fda97321c5

| condition | family | generated | completed | drained | bottleneck | max queues |
|---|---|---:|---:|---|---|---|
| generation_sweep_r1 | generation_sweep_fixed_downstream | 40 | 40 | True | generation | generation=0, evaluation=0, integration=0, maintenance=0, retirement=0 |
| generation_sweep_r2 | generation_sweep_fixed_downstream | 80 | 80 | True | generation | generation=0, evaluation=0, integration=0, maintenance=0, retirement=0 |
| generation_sweep_r4 | generation_sweep_fixed_downstream | 160 | 160 | True | generation | generation=0, evaluation=0, integration=0, maintenance=0, retirement=0 |
| generation_sweep_r8 | generation_sweep_fixed_downstream | 320 | 320 | True | evaluation | generation=0, evaluation=160, integration=0, maintenance=0, retirement=0 |
| capacity_ladder_evaluation | capacity_release_ladder | 160 | 160 | True | evaluation | generation=0, evaluation=120, integration=0, maintenance=0, retirement=0 |
| capacity_ladder_integration | capacity_release_ladder | 160 | 160 | True | integration | generation=0, evaluation=0, integration=120, maintenance=0, retirement=0 |
| capacity_ladder_maintenance | capacity_release_ladder | 160 | 160 | True | maintenance | generation=0, evaluation=0, integration=0, maintenance=120, retirement=0 |
| capacity_ladder_retirement | capacity_release_ladder | 160 | 160 | True | retirement | generation=0, evaluation=0, integration=0, maintenance=0, retirement=120 |

Boundary: synthetic instrumentation only; no deployment or general-law claim.
