# Queue migration v4 results

Status: `trace_derived_calibration`
Protocol: `queue-migration-v4`
Receipt: `artifacts/queue_migration_v4.json`
Source: `conversation/records.jsonl`
Source SHA-256: `dffc63dce4c36a12e28f5dce447ca997516a7ea4c099d3a46a5d96262053eb38`
Input SHA-256: `dc6640a5c198e5bbbfea23a47114077b29da3179e4064e7fbcc5ad1304a3d57e`
Independent audit: `passed`

## Source-derived workload

The archive contributes 1,190 timestamped records across 494 one-minute bins. Only timestamps and role labels were used. Message content was excluded from the emitted receipt and summary. The largest one-minute demand bucket contains 108 records.

## Observed bottlenecks

| condition | bottleneck | generated | source shortfall |
|---|---|---:|---:|
| generation cap 1 | generation | 201 | 989 |
| generation cap 2 | generation | 337 | 853 |
| generation cap 4 | generation | 507 | 683 |
| generation cap 8 | evaluation | 647 | 543 |
| capacity ladder: evaluation | evaluation | 1190 | 0 |
| capacity ladder: integration | integration | 1190 | 0 |
| capacity ladder: maintenance | maintenance | 1190 | 0 |
| capacity ladder: retirement | retirement | 1190 | 0 |

The high-capacity generation sweep exposes evaluation pressure despite the trace's burst structure. The capacity-release ladder localizes the active burden to each deliberately constrained downstream stage.

## Verification

The v4-specific test suite passed 3/3 tests. The runner succeeded with exit code 0. The receipt passed the independent flow audit and drained every replayed workload. A prior smoke invocation used the wrong relative source path (`../../conversation/records.jsonl`) and failed before reading input; it produced no artifact and is recorded as a harness invocation error, not a result.

## Interpretation boundary

This is one anonymized archive-trace replay, not a population estimate or field study. The source is historical, finite, and drawn from one archive. The result does not establish stationarity, participant causality, deployment relevance, organizational behavior, AI-system behavior, or a universal queueing law. It is stronger than the synthetic workload-only result because the demand schedule is source-derived, but it remains a bounded calibration.
