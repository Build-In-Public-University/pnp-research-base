# Semantic interaction calibration v1: executed results

This experiment tests the term omitted by fixed dependency coverage:

\[
D_{\mathrm{joint}}(S)
=
\bigcup_{x\in S}D(x)\cup D_{\mathrm{interaction}}(S).
\]

Twelve archive-shaped base files feed twelve derived records with join widths 1, 2, and 4. The `disjoint` and `adjacent` cases use only ordinary dependencies. The `joint` and `cluster` cases activate an explicit additional constraint on derived record 8 when inputs 0 and 1 change together.

## Results

Twelve cells were executed. The ordinary union-only policy was exact in all control cells and failed in every interaction cell. The interaction-aware policy was exact in all 12 cells.

| Case | Join width | Ordinary union | Joint affected set | Interaction nodes | Union exact | Interaction-aware exact |
|---|---:|---:|---:|---:|---|---|
| disjoint | 1 / 2 / 4 | 2 / 4 / 8 | same | 0 | yes | yes |
| adjacent | 1 / 2 / 4 | 2 / 3 / 5 | same | 0 | yes | yes |
| joint | 1 / 2 / 4 | 2 / 3 / 5 | 3 / 4 / 6 | 1 | no | yes |
| cluster | 1 / 2 / 4 | 4 / 5 / 7 | 5 / 6 / 8 | 1 | no | yes |

The failed union-only cases are deliberate. The independent oracle includes the explicit joint constraint, while the ordinary policy does not know it exists. This is the required counterexample to the assumption that the causal cone is always the union of individual cones.

## Interpretation

For the fixed-union controls, the ordinary coverage model is sufficient. For the explicit interaction cases:

\[
|D_{\mathrm{joint}}(S)|
>
\left|\bigcup_{x\in S}D(x)\right|.
\]

The additional work is not overlap. It is a new joint consequence. The result therefore distinguishes two mechanisms:

- shared dependencies produce subadditive repair through set union;
- joint constraints produce an interaction cone outside that union.

The interaction rule is synthetic and explicit. It is not inferred from natural-language semantics, and it does not establish a general law about real applications. Timing remains local diagnostic data.

## Reproduction

```sh
PYTHONPATH=src python3 -m unittest tests.test_interaction_v1 -q
PYTHONPATH=src python3 scripts/run_interaction_v1.py \
  --output artifacts/interaction_v1_local.json \
  --summary artifacts/interaction_v1_local.md
```
