# Queue migration v4 trace-2 results

Protocol: `queue-migration-v4`
Receipt: `artifacts/queue_migration_v4_trace2.json`
Source: `conversation/subagents/worker-7/records.jsonl`
Source SHA-256: `6903037bdbad8b0fc3b6d48d61e264bc8a30cbe1a3808ca9ecbb56581b067c9e`
Input SHA-256: `c50b7255a7ad3d09074c767f0c5dec8fc72c2dfc43df2da9f9615d7619ce86a4`
Independent audit: `passed`

## Results

The second trace contains 58 timestamped records. The frozen replay contract produced the following bottlenecks:

| condition | bottleneck | generated | source shortfall |
|---|---|---:|---:|
| generation cap 1 | generation | 8 | 50 |
| generation cap 2 | generation | 16 | 42 |
| generation cap 4 | generation | 32 | 26 |
| generation cap 8 | evaluation | 52 | 6 |
| capacity ladder: evaluation | evaluation | 58 | 0 |
| capacity ladder: integration | integration | 58 | 0 |
| capacity ladder: maintenance | maintenance | 58 | 0 |
| capacity ladder: retirement | retirement | 58 | 0 |

The result matches the first archive trace at the level of the declared mechanism. The generation sweep moves from generation to evaluation pressure, and the release ladder localizes the active constrained stage.

## Boundary

This is a second trace within the same exported archive corpus. It is not an independent organization, production deployment, or population sample. It strengthens trace sensitivity only. It does not establish stationarity, participant causality, deployment generality, or a universal queueing law.
