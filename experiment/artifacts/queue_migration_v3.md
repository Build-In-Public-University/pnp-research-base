# Queue migration v3 independent workload cross-check

status: synthetic_fixture
protocol: queue-migration-v3
records: 48
independent_audit: passed
input_sha256: 61aac28130fffeccb70a3bc4eff969a18c3b556e544f03e5a3579c9c13e2ce56

| workload | condition | bottleneck counts |
|---|---|---|
| burst_train | generation_sweep_r1 | {'generation': 3} |
| burst_train | generation_sweep_r2 | {'generation': 3} |
| burst_train | generation_sweep_r4 | {'generation': 3} |
| burst_train | generation_sweep_r8 | {'evaluation': 3} |
| burst_train | capacity_ladder_evaluation | {'evaluation': 3} |
| burst_train | capacity_ladder_integration | {'integration': 3} |
| burst_train | capacity_ladder_maintenance | {'maintenance': 3} |
| burst_train | capacity_ladder_retirement | {'retirement': 3} |
| jittered | generation_sweep_r1 | {'generation': 3} |
| jittered | generation_sweep_r2 | {'generation': 3} |
| jittered | generation_sweep_r4 | {'generation': 3} |
| jittered | generation_sweep_r8 | {'evaluation': 3} |
| jittered | capacity_ladder_evaluation | {'evaluation': 3} |
| jittered | capacity_ladder_integration | {'integration': 3} |
| jittered | capacity_ladder_maintenance | {'maintenance': 3} |
| jittered | capacity_ladder_retirement | {'retirement': 3} |

Boundary: independent synthetic workload cross-check only.
