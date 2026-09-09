# Fan-out calibration v1: executed results

The concrete archive-manifest calibration now includes dependency geometry. Twelve copied base files feed layered derived records. One changed base file is routed through a controlled fan-out branch; depth controls how many derived layers must be repaired.

## Matrix

Thirty cells were executed: fan-outs `1, 2, 4, 8, 11`, depths `1, 2, 4`, and assurance scopes `full` and `affected`. The affected fraction is:

| Fan-out | Depth | Affected fraction | Incremental repair nodes |
|---:|---:|---:|---:|
| 1 | 1/2/4 | 0.083 | 1/2/4 |
| 2 | 1/2/4 | 0.167 | 2/4/8 |
| 4 | 1/2/4 | 0.333 | 4/8/16 |
| 8 | 1/2/4 | 0.667 | 8/16/32 |
| 11 | 1/2/4 | 0.917 | 11/22/44 |

Every full-recompute and indexed-incremental result was mechanically exact against an independent full oracle.

## Interpretation

The repair scope follows the transitive affected set:

\[
|D(\Delta S)| = \text{fan-out} \times \text{depth}
\]

for this deliberately controlled graph. The affected fraction \(\rho\) therefore moves from 0.083 to 0.917 without changing the base-file count.

Full assurance validates all derived nodes in every cell. Affected-only assurance validates only the repaired branch; it is reported separately and must not be described as equivalent global assurance. This separation keeps maintenance cost distinct from assurance cost.

The calibration supports a narrow statement: dependency geometry determines how many derived records a local change must repair in this workload. It does not establish that incremental repair is faster end-to-end, because index, filesystem, serialization, transport, and assurance costs remain separate. Timing is machine-local diagnostic data.

The next useful boundary is the approach to \(\rho=1\): increase fan-out to the entire graph and add index-maintenance and multi-input join costs. The predicted crossover is a hypothesis, not an observed runtime claim yet.

## Reproduction

```sh
PYTHONPATH=src python3 -m unittest tests.test_fanout_v1 -q
PYTHONPATH=src python3 scripts/run_fanout_v1.py \
  --output artifacts/fanout_v1_local.json \
  --summary artifacts/fanout_v1_local.md
```

The archive is copied to temporary storage and never modified. Receipt: `artifacts/fanout_v1_run1.json`; summary: `artifacts/fanout_v1_run1.md`.
