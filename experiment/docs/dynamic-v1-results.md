# Dynamic dependency repair v1: executed results

## Result

The dynamic-dependency experiment is implemented and executed locally with two byte-identical persistent receipts. It compares cold recomputation, visible selective repair, visible full reset, certificate-validated repair, and an unchecked cache control under changing state and dependency graphs.

The bounded result is:

> Selective repair can reduce output recomputation when the dependency view is complete, but it cannot protect against dependency drift that remains invisible to that view. A certificate validation channel can detect the hidden drift in this fixture and restore exactness, at additional modeled validation and repair cost. Full reset is not safe against a change it cannot observe.

This is a conditional mechanism result for a finite synthetic dependency system. It is not a runtime, deployment, energy, economic, lower-bound, or P/NP result.

## Frozen sweep

The sweep contains **144 matched cells**:

- sizes `n = 8, 16`;
- state changes per step `0, 1, n/2, n`;
- graph changes per step `0, n/2, n`;
- seeds `1, 7, 19`;
- visible and hidden dependency drift.

Each cell has eight time points: an initial state plus seven updates. The actual dependency graph is used only by the independent oracle and by the certificate policy after validation. Ordinary selective repair sees only the visible graph/version. Hidden drift changes the actual graph while leaving the visible graph/version unchanged.

## Aggregate outcomes

| Policy | Operations | Wrong outputs | Stale acceptances |
|---|---:|---:|---:|
| cold recompute | 104,832 | 0 | 0 |
| selective repair | 258,602 | 47 | 12 |
| full reset | 194,688 | 47 | 0 |
| certificate repair | 262,940 | 0 | 0 |
| unchecked cache | 22,932 | 1,044 | 1,044 |

Operations are the sum of declared logical counters. They include metadata discovery, state/index work, certificate validation, output reads/writes, and arithmetic additions. They exclude world generation, oracle execution, validation-channel production, serialization, runtime, energy, and hardware effects.

The strict exactness winner count is not a recommendation: cold recomputation is the least-operation exact policy in 132 cells; selective repair and full reset are exact and least-operation in 12 cells each. The unchecked cache ties for least operations in 12 cells only because it is unsafe in the other dimensions of the contract.

## What the controls show

- Under complete visibility, selective repair can touch only affected outputs instead of recomputing the full vector.
- Under hidden graph drift, selective repair can return a stale vector while its visible inputs appear unchanged. The 12 recorded stale acceptances are detected by the external oracle classification, not by the ordinary policy itself.
- Full reset protects against visible changes but cannot reset for an invisible change. Its 47 wrong outputs are therefore a boundary result, not an implementation surprise.
- Certificate repair validates the graph digest, identifies affected outputs, and returns the oracle result in every cell. The certificate is a modeled validation channel, not proof that the issuer or digest represents semantic truth.
- The unchecked control is cheap because it omits invalidation and repair. Its 1,044 wrong outputs are deliberately retained as the safety cost of that shortcut.

## Falsifiers and limitations

The result would weaken if selective repair failed to reduce modeled work in low-churn cells after discovery and index costs, or if certificate repair failed to restore exactness after hidden drift. The current fixture supports neither a universal selective-repair advantage nor a claim that certificate validation is cheaper; certificate repair has the highest total modeled operation count in this sweep.

The hidden graph digest is supplied as a validation input. It does not model key custody, adversarial issuer behavior, network failures, serialization cost, or an actual deployment. The generated trajectories are paired by seed and should not be treated as independent population samples. The cost weights are synthetic.

Open extensions remain:

- separate dependency discovery from an independently measured graph-construction cost;
- add partial or delayed certificate delivery rather than an always-available digest;
- compare selective repair against full reset under visible high churn without hidden drift;
- add explicit stale-result consequence penalties and downstream repair costs;
- calibrate the counters against one concrete application before interpreting any phase boundary.

## Reproduction

From the experiment root:

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -q
PYTHONPATH=src python3 scripts/run_dynamic.py \
  --output artifacts/dynamic_v1_local.json \
  --summary artifacts/dynamic_v1_local.md
```

The runner refuses to overwrite existing files. Use another fresh output path for a repeat and compare both JSON and Markdown with `cmp`.

Receipts:

- `artifacts/dynamic_v1_run1.json` — `cebae211c7cca4ce7a081bad149af81a86263d6b74f7ea6968ce8415c6e3dad4`
- `artifacts/dynamic_v1_run1.md` — `4067585503a03b9b987cdf7ac259675507852ff4e9d3887214aed7516fdc93cf`
- `artifacts/dynamic_v1_run2.json` — byte-identical to run 1
- `artifacts/dynamic_v1_run2.md` — byte-identical to run 1

The implementation and protocol are `src/pnp_architecture/dynamic.py` and `docs/protocol-dynamic-dependencies-v1.md`.
