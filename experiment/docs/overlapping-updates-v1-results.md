# Overlapping updates calibration v1: executed results

This calibration changes multiple archive-manifest inputs simultaneously. Twelve derived records join contiguous base inputs at widths 1, 2, and 4. Four update patterns were tested: one input, two disjoint inputs, two adjacent inputs, and a four-input cluster. Assurance scopes were full and affected-only.

## Result

Twenty-four cells were executed. Every indexed-incremental output was mechanically exact against an independent full oracle.

| Pattern | Join width | Isolated affected sum | Union affected set | Overlap savings |
|---|---:|---:|---:|---:|
| single | 1/2/4 | 1/2/4 | 1/2/4 | 0 |
| disjoint | 1/2/4 | 2/4/8 | 2/4/8 | 0 |
| adjacent | 1 | 2 | 2 | 0 |
| adjacent | 2 | 4 | 3 | 1 |
| adjacent | 4 | 8 | 5 | 3 |
| cluster | 1 | 4 | 4 | 0 |
| cluster | 2 | 8 | 5 | 3 |
| cluster | 4 | 16 | 7 | 9 |

The result is the expected union correction:

\[
|D(\Delta x_1)\cup D(\Delta x_2)|
\leq
|D(\Delta x_1)|+|D(\Delta x_2)|
\]

For adjacent updates, join width creates shared affected records. At join width 4, the four-input cluster has an isolated sum of 16 but a union of 7, saving 9 redundant repair records.

Disjoint and single-input patterns are controls. They produce no overlap savings, preventing the harness from treating every multi-update workload as a union advantage.

## Boundary

This supports a narrow architectural statement: for simultaneous changes, repair cost is governed by the union of affected dependency sets, not the sum of independently estimated fan-outs. It does not establish an end-to-end timing advantage. Reverse-index maintenance, assurance, serialization, transport, and downstream consequences remain separate costs.

## Reproduction

```sh
PYTHONPATH=src python3 -m unittest tests.test_overlap_v1 -q
PYTHONPATH=src python3 scripts/run_overlap_v1.py \
  --output artifacts/overlap_v1_local.json \
  --summary artifacts/overlap_v1_local.md
```

The archive is copied to temporary storage and never modified. Receipt: `artifacts/overlap_v1_run1.json`; summary: `artifacts/overlap_v1_run1.md`.
