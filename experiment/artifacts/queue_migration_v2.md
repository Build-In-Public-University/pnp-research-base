# Queue migration v2 synthetic fixture

status: synthetic_fixture
protocol: queue-migration-v2
seeds: [0, 1, 2, 3, 4]
input_sha256: 2d8ea736480c7416ae7fd18eaa9cbf6c093bd4352f845946b6369f60ca416e7a
independent_audit: passed

| condition | seeds | bottleneck counts | stationarity diagnostics |
|---|---:|---|---|
| generation_sweep_r1 | 5 | {'generation': 5} | 5/5 pass |
| generation_sweep_r2 | 5 | {'generation': 5} | 5/5 pass |
| generation_sweep_r4 | 5 | {'generation': 5} | 5/5 pass |
| generation_sweep_r8 | 5 | {'evaluation': 5} | 5/5 pass |
| capacity_ladder_evaluation | 5 | {'evaluation': 5} | 5/5 pass |
| capacity_ladder_integration | 5 | {'integration': 5} | 5/5 pass |
| capacity_ladder_maintenance | 5 | {'maintenance': 5} | 5/5 pass |
| capacity_ladder_retirement | 5 | {'retirement': 5} | 5/5 pass |

Boundary: synthetic instrumentation only; no deployment or general-law claim.
