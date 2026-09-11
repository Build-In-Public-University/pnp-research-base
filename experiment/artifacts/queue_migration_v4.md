# Queue migration v4 trace-derived calibration

status: trace_derived_calibration
protocol: queue-migration-v4
trace_records: 1190
trace_sha256: dffc63dce4c36a12e28f5dce447ca997516a7ea4c099d3a46a5d96262053eb38
independent_audit: passed
input_sha256: dc6640a5c198e5bbbfea23a47114077b29da3179e4064e7fbcc5ad1304a3d57e

| condition | bottleneck | generated | source shortfall |
|---|---|---:|---:|
| generation_sweep_cap1 | generation | 201 | 989 |
| generation_sweep_cap2 | generation | 337 | 853 |
| generation_sweep_cap4 | generation | 507 | 683 |
| generation_sweep_cap8 | evaluation | 647 | 543 |
| capacity_ladder_evaluation | evaluation | 1190 | 0 |
| capacity_ladder_integration | integration | 1190 | 0 |
| capacity_ladder_maintenance | maintenance | 1190 | 0 |
| capacity_ladder_retirement | retirement | 1190 | 0 |

Boundary: one anonymized archive trace replay; no participant or deployment claim.
