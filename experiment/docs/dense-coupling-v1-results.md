# Dense-coupling calibration v1: executed results

This calibration extends the archive-manifest workload with multi-input joins. Twelve copied base files feed twelve derived records. One changed base file affects a controlled fan-out branch; each derived record has join width `j`.

## Matrix

Thirty cells varied fan-out `1,2,4,8,11`, join width `1,2,4`, and assurance scope `full,affected`. Every indexed-incremental result was mechanically exact against an independent full oracle.

The accounting identities held in every cell:

\[
E_{\mathrm{index}} = |V|\times j
\]

\[
E_{\mathrm{affected}} = |D(\Delta S)|\times j
\]

For example, at fan-out 1 and join width 4, full repair performs 48 edge checks while incremental repair performs 4. At fan-out 11 and join width 4, the counts are 48 and 44. The reduction therefore tracks affected fraction \(\rho\), not merely input count.

| Fan-out | \(\rho\) | Incremental repair nodes at depth 1 | Incremental edge checks for join width 1/2/4 |
|---:|---:|---:|---:|
| 1 | 0.083 | 1 | 1 / 2 / 4 |
| 2 | 0.167 | 2 | 2 / 4 / 8 |
| 4 | 0.333 | 4 | 4 / 8 / 16 |
| 8 | 0.667 | 8 | 8 / 16 / 32 |
| 11 | 0.917 | 11 | 11 / 22 / 44 |

Full assurance remains separate from affected-only assurance. Affected-only checking is not equivalent to global assurance. Wall-clock timing is local diagnostic data over temporary copies and is not evidence of distributed or universal performance.

## Boundary

The calibration supports a narrow architectural statement: dependency geometry determines both the number of derived records and the number of parent edges that must be revisited after a local change. As \(\rho\) approaches one, the edge-check reduction approaches one as well. Whether incremental repair wins total cost still depends on index maintenance, assurance scope, serialization, transport, and downstream consequences.

The next gate is a multi-input update workload where several bases change together and affected branches overlap. That will test whether the union of affected dependency sets, rather than the sum of isolated fan-outs, controls repair cost.

## Reproduction

```sh
PYTHONPATH=src python3 -m unittest tests.test_dense_coupling_v1 -q
PYTHONPATH=src python3 scripts/run_dense_coupling_v1.py \
  --output artifacts/dense_coupling_v1_local.json \
  --summary artifacts/dense_coupling_v1_local.md
```

The archive is copied to temporary storage and never modified. Receipt: `artifacts/dense_coupling_v1_run1.json`; summary: `artifacts/dense_coupling_v1_run1.md`.
