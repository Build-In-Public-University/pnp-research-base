# Dynamic dependency consequence v2: executed results

## Result

Version 2 extends dynamic dependency repair v1 with partial/delayed certificate availability and a deterministic consequence model for stale reuse. Two byte-identical JSON receipts and two byte-identical Markdown summaries were produced.

The bounded result is:

> Validation can become preferable only after stale reuse is assigned a consequence cost. Complete certificate validation prevents stale outputs in this fixture, but is more expensive when stale consequences are priced at zero. Delayed validation occupies a middle position: it reduces unsafe reuse relative to visible selective repair, but still permits stale outputs between certificate arrivals.

This is a finite synthetic mechanism test. It is not an incident probability, deployment result, runtime measurement, energy result, or P/NP evidence.

## Frozen sweep

The sweep contains **288 matched cells**:

- sizes `n = 8, 16`;
- state changes per step `0, 1, n/2, n`;
- graph changes per step `0, n/2, n`;
- seeds `1, 7, 19`;
- certificate intervals `1, 3`;
- hidden and visible dependency drift.

Each cell contains an initial state plus seven updates. The certificate policy validates every update. The delayed policy validates only at its declared interval and uses the visible dependency view between validations. The independent oracle always evaluates the actual dependency graph.

The default consequence model uses stale-failure rate `0.25` and downstream-repair penalty `100`. Stale failures are deterministic fixture outcomes, not estimates of real-world likelihood.

## Aggregate default-cost outcomes

| Policy | Total modeled cost | Wrong outputs | Unsafe reuse | Stale failures |
|---|---:|---:|---:|---:|
| selective repair | 629,624 | 766 | 766 | 1,408 |
| certificate repair | 534,520 | 0 | 0 | 0 |
| delayed certificate | 566,749 | 293 | 293 | 401 |
| unchecked cache | 533,664 | 2,088 | 2,088 | 4,878 |

`Total modeled cost` is declared logical operation cost plus stale-failure consequence cost. The unchecked cache is slightly cheaper than certificate repair at the default penalty only because it omits the validation and repair work; that does not make it safe.

## Consequence break-even surface

The surface counts least-modeled-cost winners across all 288 cells. Ties are credited to every tied policy.

| Consequence penalty | Selective | Certificate | Delayed certificate | Unchecked |
|---:|---:|---:|---:|---:|
| 0 | 48 | 0 | 0 | 288 |
| 10 | 48 | 0 | 0 | 288 |
| 100 | 106 | 44 | 23 | 168 |
| 1,000 | 192 | 96 | 50 | 24 |
| 10,000 | 192 | 96 | 50 | 24 |

The penalty surface is conditional on this fixture, counter weights, certificate intervals, stale-failure rule, and downstream penalty semantics. It is not a universal break-even threshold.

## What the controls show

- Complete certificate repair is exact in every cell and records no unsafe reuse.
- Delayed validation reduces stale exposure relative to selective repair but cannot prevent stale output during the interval without a certificate.
- Selective repair remains cheaper in some cells even after consequences are priced. It is not dominated universally.
- Unchecked reuse wins when correctness consequences are free or nearly free. That is an accounting result, not an engineering recommendation.
- The zero-drift control makes certificate validation a pure modeled cost, preserving the null against validation being declared universally beneficial.

## Limitations and next gate

The certificate digest is a modeled validation input. It does not model key custody, adversarial issuers, delivery failure, serialization, network delay, human review, or a real application. The stale-failure rate and downstream penalty are synthetic. Cells sharing a trajectory are paired observations, not independent samples.

The next gate is calibration against one concrete application: measure local recomputation, dependency discovery, certificate production/validation, serialization, and downstream repair on a frozen workload. Keep the synthetic receipts unchanged and write a separate measured replay. Do not use calibrated numbers to silently replace this model.

## Reproduction

From the experiment root:

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -q
PYTHONPATH=src python3 scripts/run_dynamic_v2.py \
  --output artifacts/dynamic_v2_local.json \
  --summary artifacts/dynamic_v2_local.md
```

The runner refuses to overwrite existing files. Use fresh paths for repeats and compare JSON and Markdown with `cmp`.

Receipts:

- `artifacts/dynamic_v2_run1.json` — `dbd0e08ed9481bfbeec0cb16ea44b0df656026af239532a33cca2ea968aa63d0`
- `artifacts/dynamic_v2_run1.md` — `4d1637d71157a9a3a734e81e941fbb9ec7390dcbfb97c3a498a417e13553791b`
- `artifacts/dynamic_v2_run2.json` — byte-identical to run 1
- `artifacts/dynamic_v2_run2.md` — byte-identical to run 1

Implementation and protocol:

- `src/pnp_architecture/dynamic_v2.py`
- `docs/protocol-dynamic-dependencies-v2.md`
