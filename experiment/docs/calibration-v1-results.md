# Concrete calibration v1: archive manifest integrity results

## Measured result

The synthetic dynamic-dependency model was calibrated against a concrete local application: validating the SHA-256 manifest of this public research archive. The benchmark copied 24 existing manifest-backed files into a temporary directory and applied four one-file updates. The public checkout was not modified.

| Arm | Files hashed | Invalidated records | Transport bytes | Full verification ns |
|---|---:|---:|---:|---:|
| full recompute | 96 | 96 | 332 | 14,784,501 |
| indexed incremental | 4 | 4 | 332 | 15,122,459 |

Both arms were mechanically exact on all four updates. Incremental repair hashed 4 changed-file instances instead of 96, while the independent full-verification check remained present in both arms. That check is intentionally not omitted or attributed to the incremental saving.

## Phase accounting

The receipt contains separate wall-clock nanoseconds and counts for dependency discovery, graph/index construction, update detection, certificate production, certificate validation, transport serialization, invalidation, repair, and full verification. The measured result is machine-local Python/filesystem behavior over temporary copies. It does not measure a distributed network, production traffic, provider latency, energy, or security guarantees.

## Interpretation boundary

This calibration supports a narrow instrument statement: for this archive-manifest workload, a one-file update can reduce the number of files hashed by indexed repair while preserving mechanical exactness. It does not establish that indexed repair is faster overall—the measured full-verification times are close and noisy at this scale—or that the mechanism generalizes to other applications.

The next calibration should increase repeated work and resolution before interpreting timing differences, and should add a concrete dependency join where one changed file invalidates multiple derived records. The synthetic v1/v2 receipts remain the mechanism tests; this measured receipt is separate evidence.

## Reproduction

From the experiment root:

```sh
PYTHONPATH=src python3 -m unittest tests.test_calibration_v1 -q
PYTHONPATH=src python3 scripts/run_calibration_v1.py \
  --output artifacts/calibration_v1_local.json \
  --summary artifacts/calibration_v1_local.md
```

The runner refuses to overwrite existing paths. Receipt: `artifacts/calibration_v1_run1.json`. Summary: `artifacts/calibration_v1_run1.md`.
