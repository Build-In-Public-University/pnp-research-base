# Staged release v1: executed local results

**Outcome:** 492 safe-policy rows covering **78,240 candidate-recipient decisions** exactly match the independent `math.gcd`/sum oracle. No safe false accepts, false rejects or unavailable results in the complete-data sweep. Reuse has both substantial modeled wins and communication/hash-driven losses. This is **TRUSTED ATTESTATION**, not a succinct proof of mathematical truth.

## Scope and primary results

164 matched cells, eight candidates each, five policies, **820 policy rows**. Primary: N=1,4,16,64 × sizes 8,32 × seeds 1,7,19 × all-valid/mixed × local compatibility all/half/none = 144 cells. Another 20 cells test post-approval content mutation, dependency/version/scope changes and local contract mismatch. All safe fault decisions remain exact through independent recomputation where evidence is stale. No hidden oracle labels enter policy decisions.

| Policy versus broad | Compute-only wins/ties/losses | Total unit-weight wins/ties/losses |
|---|---:|---:|
| Upstream gate, independent downstream checks | 36/0/108 | 45/0/99 |
| Upstream attestation + real local checks | 108/0/36 | 54/0/90 |

These comparisons cover 144 primary cells. The honest cost boundary is not universal superiority: evidence can remove duplicate shared computation while adding more byte-processing/transmission cost than it saves.

Representative seed-7 results:

| Workload | Policy | Compute | Total unit-weight | Full-payload recipient exposures | Shared checks |
|---|---|---:|---:|---:|---:|
| N=1, size=8, all-valid, all-local | broad | 1,952 | 2,773 | 8 | 8 |
| same | gate | 3,832 | 5,482 | 8 | 16 |
| same | attested | 2,008 | 10,180 | 8 | 8 |
| N=64, size=8, all-valid, all-local | broad | 124,928 | 177,472 | 512 | 512 |
| same | attested | 9,568 | 338,914 | 512 | 8 |
| N=64, size=32, all-valid, all-local | broad | 2,099,584 | 2,207,296 | 512 | 512 |
| same | gate | 2,132,126 | 2,242,033 | 512 | 520 |
| same | attested | 52,518 | 493,924 | 512 | 8 |
| N=64, size=32, mixed, half-local | broad | 1,108,224 | 1,216,000 | 512 | 512 |
| same | gate | 1,052,640 | 1,108,596 | 256 | 264 |
| same | attested | 27,172 | 248,780 | 256 | 8 |

Local compatibility was swept separately with genuine downstream sum/budget checks. Since all safe policies check shared before local and sum all vector elements regardless of budget, local rejection changes eligibility but not the predicate-work count in matched cells. The zero-compatible regime therefore still pays validation cost: technical shared validity is not recipient utility.

## Controls and trust boundary

Across all cells the unsafe skip-local policy produced **9,540 false accepts**; the injected domain-only weak upstream produced **3,456**, with **64 recipients** falsely accepting a single bad candidate in the largest common-mode control. These deliberately injected counts are NOT real incident probabilities. Both controls had zero false rejects/unavailable in this bounded complete-data fixture.

Recipients receive the full current artifact, current authoritative local budget and (where applicable) content-bound shared evidence. Evidence asserts only the shared coprimality predicate, not recipient-local contracts. SHA-256 plus HMAC binds content/scope/dependency/version to an issuer assertion. The HMAC key is a **public laboratory fixture**, so authentication is simulated; secret-key custody is an explicit deployment assumption. Even secure authentication cannot prove the issuer computed the predicate correctly. Scope/dependency/version metadata are assumed authoritative and visible, not discovery of hidden freshness. Dependency contents themselves are not validated.

Evidence mismatch falls back to the full shared predicate, then still checks local eligibility. Missing payload or local contract returns unavailable in receiver tests and is not included in complete-data equivalence. Upstream rejection remains sound only for this frozen mutation family, which never repairs originally invalid artifacts after the gate.

## Cost interpretation and exclusions

Actual loop counters include domain tests, pair tests, Euclidean modulo iterations, local sum additions/comparisons, metadata comparisons, and authentication invocations. Every full validator uses the identical early-exit GCD algorithm; the baseline is not algorithmically handicapped. Hash bytes, HMAC message bytes and actual canonical-JSON payload/evidence/status bytes are separately charged. Producer-to-upstream delivery, evidence creation and per-recipient verification are included.

`compute_only` excludes all per-byte work; `total_unit_weight` adds hash bytes, HMAC message bytes, and communication bytes at unit weight. These are uncalibrated mixed-unit sensitivities, **not measured timing, money or energy**. Setup inventory and assumed generation of one unit per materialized integer are separate and identical across policies. Excluded: actual fixed-prime-pool generation, RNG, Python allocations, serialization CPU, oracle scoring, receipt/provenance hashing and I/O, context discovery, key provisioning/rotation, network framing/encryption/retries, latency/parallel hardware, energy and labor. HMAC internal padding/key expansion is not counted per byte. These exclusions prevent an end-to-end cost claim.

## Freeze, execution and persistence

Protocol SHA-256, frozen before implementation/results:
`cfcde3a83183beb112a168c5fc27b27209a730c06cf325d5769eb80158cb1ab4`.

Tests were written first. Initial missing-module import was a **setup failure, not behavioral RED**. A minimal shared-predicate stub then failed the actual valid-vector assertion (`False is not true` on `[5,7,11]`). Remaining tests were specified before implementation; this is not a claim that each separately underwent behavioral RED.

`python -m unittest discover -s tests -p test_release.py -v`: **10 passed**, 39.704 seconds. Covers the full safe grid, arithmetic counters, all fault types, local mismatch, missing data, tampered attestation, unsafe controls, seed variation, freeze integrity, two temporary CLI runs, overwrite refusal, and source-hash/output readback. Only this test file was run by this lane; parent owns whole-suite audit.

Independent persistent executions:

```
python scripts/run_release.py --prefix artifacts/release_v1_run1
python scripts/run_release.py --prefix artifacts/release_v1_run2
```

Both report `164 cells; 820 rows; safe exact equivalence verified`.

- JSON pair: **7,492,047 bytes each**, SHA-256 `f71a13eb4379b59a00db448ce6472bc8f891b020f81615585e93834d7c59bf2e`.
- Markdown pair: **4,286 bytes each**, SHA-256 `9852cea1c8d0f1f66ba274a5bda2a8e864a70c5ad611c4a151afd539bf27fc86`.
- Independent readback asserted both pairs byte-identical and verified every embedded source hash against disk. Outputs use exclusive creation, never overwrite. JSON embeds complete fixtures/decisions/counters plus module path and source SHA-256 values. No timestamps or output-prefix strings contaminate deterministic content.
- Imported module: `<HOME>/pnp-network-architecture/src/pnp_architecture/release.py`.
- Module SHA-256: `909a240a7b4dd671cc22aaeb967f157d9aea413adfff31f195af4d35287d3927`.

A report-assembly helper encountered a tool-return-shape `KeyError` after successful receipt verification; it did not write or alter any receipt. This document was then written directly. No experiment execution failures or test failures remained.

## Post-run lint-only provenance amendment

Parent pre-commit Pyflakes checking found two unused imports (`math`, `os`) in the release test file. They were removed; no predicate, policy, fixture, counter, protocol or assertion changed. The exact original test source is preserved in `artifacts/release_v1-test-source.txt`, matching the original receipts' test hash. Original receipts remain untouched.

The parent then executed `artifacts/release_v1_verified1.json` and `artifacts/release_v1_verified2.json`: byte-identical SHA-256 `4fb85178fcb6885b644defdf844321273b0eaa8905cb2169c624834cbca1b2cb`. The only JSON difference from the original run is the test-source hash; every fixture, decision and cost is identical. These new receipts match all current source hashes. Markdown summaries remain byte-identical to the originals. Independent audit explicitly verifies both the archived original test source and the current reviewed source rather than hiding the provenance change.

Final parent suite: 76 tests passed (`artifacts/situated_v1-final-tests.txt`); Pyflakes F checks pass on all new Python files, and mypy's non-strict check with skipped imports passes on the six new implementation/runner files. Neither substitutes for the independent oracle audit.

## Exact owned file inventory

1. `src/pnp_architecture/release.py`
2. `scripts/run_release.py`
3. `tests/test_release.py`
4. `docs/protocol-release-v1.md`
5. `docs/protocol-release-v1.md.sha256`
6. `docs/release-v1-results.md`
7. `artifacts/release_v1_run1.json`
8. `artifacts/release_v1_run1.md`
9. `artifacts/release_v1_run2.json`
10. `artifacts/release_v1_run2.md`

No installs, network calls, commits, shared README or claim edits. This is conditional validation amortization and common-mode failure analysis, not P versus NP, proof compression, deployed network performance or external-action authority.
