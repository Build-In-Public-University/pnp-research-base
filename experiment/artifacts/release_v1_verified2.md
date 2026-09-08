# Staged-release v1 results

**LOCAL modeled-cost experiment; TRUSTED ATTESTATION, not a succinct proof of truth.**

164 matched cells; 820 policy rows; 144 primary cells and 20 fault cells.
Eight candidates per cell; five policies. All fixtures, decisions and counters are in the JSON receipt.

## Correctness

| Policy | False accepts | False rejects | Unavailable |
|---|---:|---:|---:|
| broad | 0 | 0 | 0 |
| gate | 0 | 0 | 0 |
| attested | 0 | 0 | 0 |
| skip_local | 9540 | 0 | 0 |
| weak_upstream | 3456 | 0 | 0 |

All safe-policy decisions match the independent oracle, including every available fault case.
Unsafe controls are deliberately injected common-validator or local-omission faults, not incident-rate measurements.

## Primary cost wins/ties/losses versus broad

| Policy | Compute wins/ties/losses | Total unit-weight wins/ties/losses |
|---|---|---|
| gate | 36/0/108 | 45/0/99 |
| attested | 108/0/36 | 54/0/90 |
| skip_local | 144/0/0 | 54/0/90 |
| weak_upstream | 144/0/0 | 72/0/72 |

Unsafe controls are not eligible cost winners; their costs are shown only as ablations.

## Representative safe-policy wins AND losses

| N | Size | Validity | Local | Policy | Compute | Total | Exposure | Shared checks |
|---:|---:|---|---|---|---:|---:|---:|---:|
| 1 | 8 | all | all | broad | 1952 | 2773 | 8 | 8 |
| 1 | 8 | all | all | gate | 3832 | 5482 | 8 | 16 |
| 1 | 8 | all | all | attested | 2008 | 10180 | 8 | 8 |
| 64 | 8 | all | all | broad | 124928 | 177472 | 512 | 512 |
| 64 | 8 | all | all | gate | 126808 | 180685 | 512 | 520 |
| 64 | 8 | all | all | attested | 9568 | 338914 | 512 | 8 |
| 64 | 32 | all | all | broad | 2099584 | 2207296 | 512 | 512 |
| 64 | 32 | all | all | gate | 2132126 | 2242033 | 512 | 520 |
| 64 | 32 | all | all | attested | 52518 | 493924 | 512 | 8 |
| 64 | 32 | mixed | half | broad | 1108224 | 1216000 | 512 | 512 |
| 64 | 32 | mixed | half | gate | 1052640 | 1108596 | 256 | 264 |
| 64 | 32 | mixed | half | attested | 27172 | 248780 | 256 | 8 |
| 64 | 32 | all | none | broad | 2099584 | 2207296 | 512 | 512 |
| 64 | 32 | all | none | gate | 2132126 | 2242033 | 512 | 520 |
| 64 | 32 | all | none | attested | 52518 | 493924 | 512 | 8 |

## Boundary and accounting

Compute-only counts domain/pair/modulo/local/metadata operations and authentication invocations; it excludes per-byte work. Total adds SHA content bytes, HMAC message bytes, and transmitted payload/evidence/status bytes at unit weight. These are uncalibrated mixed-unit sensitivities, not wall-clock speedups.
Receipt counters split setup, upstream, downstream and communication. Materialization/generation assumption is one unit per integer, separate from validation totals and matched across policies. Actual prime-pool generation, RNG, serialization CPU, oracle, provenance/receipt I/O, allocation, network framing/encryption/retries, key provisioning, authoritative context acquisition, energy and labor are excluded. HMAC internal padding/key expansion is not counted per byte.
HMAC uses a public deterministic laboratory key: origin authentication is simulated, not deployed security. Even real secret-key authentication binds an assertion, not its truth. Recipients see the full current artifact, evidence and current local budget; no oracle labels. Stale evidence falls back to independent checking. Shared evidence never covers recipient-local budgets.
Fault metadata is authoritative and visible by assumption; hidden stale dependencies are not solved. Upstream rejects remain sound only because the bounded downstream mutation never repairs a previously invalid artifact. Missing payload/contract is unavailable, tested separately, not claimed equivalent to a complete-data oracle.
This demonstrates conditional amortization and common-mode failure exposure, not P versus NP, mathematical proof compression, external-action authorization, real network performance or incident probabilities.

## Reproducibility

Frozen protocol SHA-256: `cfcde3a83183beb112a168c5fc27b27209a730c06cf325d5769eb80158cb1ab4`.
JSON embeds the source hashes and exact imported module path. Runner uses exclusive output creation and reads back both JSON and Markdown. Independent run prefixes have byte-identical content; timestamps and prefix names are intentionally absent.
