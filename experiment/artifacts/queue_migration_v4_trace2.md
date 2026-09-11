# Queue migration v4 trace-derived calibration

status: trace_derived_calibration
protocol: queue-migration-v4
trace_records: 58
trace_sha256: 6903037bdbad8b0fc3b6d48d61e264bc8a30cbe1a3808ca9ecbb56581b067c9e
independent_audit: passed
input_sha256: c50b7255a7ad3d09074c767f0c5dec8fc72c2dfc43df2da9f9615d7619ce86a4

| condition | bottleneck | generated | source shortfall |
|---|---|---:|---:|
| generation_sweep_cap1 | generation | 8 | 50 |
| generation_sweep_cap2 | generation | 16 | 42 |
| generation_sweep_cap4 | generation | 32 | 26 |
| generation_sweep_cap8 | evaluation | 52 | 6 |
| capacity_ladder_evaluation | evaluation | 58 | 0 |
| capacity_ladder_integration | integration | 58 | 0 |
| capacity_ladder_maintenance | maintenance | 58 | 0 |
| capacity_ladder_retirement | retirement | 58 | 0 |

Boundary: one anonymized archive trace replay; no participant or deployment claim.
