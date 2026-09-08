# Situated computation v1: observation, information and release

## Executed result

The next experiment set is implemented, run and independently audited locally. **76 repository tests pass.** New code does not replace history v1.1, gate or graph/SAT receipts. Frozen protocols precede result runs; freezes are local procedural records, not externally timestamped preregistrations.

The bounded conclusion is:

> Shared validation can reduce duplicated work after release. Observation and applicability machinery decide whether that reuse is justified. Their cost can erase the saving, and their shared failure can amplify error.

This supports a conditional operational mechanism, not a theorem that small networks always validate better or a change to P/NP.

## 1. Deployment as gated information flow

164 matched cells, 820 policy rows; **78,240 safe candidate-recipient decisions** agree with an independent oracle. Three safe policies: broad independent validation; upstream rejection gate with survivors independently rechecked; upstream gate plus content-bound trusted attestation and genuine local checks. Two unsafe controls skip local checking or use a faulty shared validator.

Representative N=64 recipients, eight valid candidates, seed 7, all local budgets compatible:

| Vector size | Broad total | Attested total | Shared checks broad → attested |
|---:|---:|---:|---:|
| 8 | 177,472 | 338,914 | 512 → 8 |
| 32 | 2,207,296 | 493,924 | 512 → 8 |

Under the declared mixed-unit total, size 32 is a **4.47-fold modeled reduction**, while size 8 is a loss despite eliminating the same duplicate shared checks. Communication and hash/authentication message processing have not been treated as free. Across 144 primary cells, attestation wins 54 and loses 90 on that total; compute-only wins 108 and loses 36. These grid counts are not prevalence estimates.

For size 32, N=64, mixed shared validity, half local compatibility, upstream filtering cuts full-payload recipient exposures from 512 to 256. Gate-only total is 1,108,596 versus broad 1,216,000; attestation is 248,780. Rejection containment and evidence reuse are separate mechanisms.

The skip-local control yields 9,540 false accepts, and faulty shared validation yields 3,456; one bad artifact reaches 64 false acceptances in the largest common-mode control. These are deliberately constructed failure counts, not estimated risks. Content hashing and authentication do not certify truth.

The source of shared evidence is represented by one trusted issuer, not a simulated human review community. Downstream fanout is explicit candidate-recipient iteration with payload accounting, not a measured packet network or a comparison of internal validator-network topologies. The experiment does not prove small-network size causes better validation.

See `docs/release-v1-results.md` and `artifacts/release_v1_run1.json`.

## 2. Observation is now produced and paid for

24 trajectories, 96 cells, **6,144 policy-tick decisions**. Event logging includes producer writes/logging, current sequence checkpoints, transport, receiver checking and snapshot recovery after gaps. Snapshot comparison and polling use the same worlds.

For n=64, seed 7, exact-vector contract, 16 ticks:

- One change/tick: complete log **1,817**, snapshot **6,382**.
- One change/tick with every fifth event dropped: log/recovery **2,792**, snapshot **6,382**, both fully correct.
- Sixteen changes/tick: complete log **5,417**, snapshot **6,832**.
- The same sixteen-change world with event loss: log/recovery **10,160**, snapshot **6,832**. Recovery reverses the ranking.
- All 64 coordinates change: even complete log **16,937** loses to snapshot **8,272**.

These are executed, declared logical counters, not runtime. They cannot be numerically compared to history v1.1's different workload and counter scheme.

Guarded periodic polling correctly answers **192/768 exact-vector requests**, versus **334/768 threshold requests** on the same paired worlds. No wrong emitted answers, but 576 and 434 unmet requests respectively. A smaller contract permits additional justified reuse; abstention does not make a policy a successful full-service solver.

Unchecked polling answers everything, with 432 wrong exact vectors and 40 wrong threshold answers. Critically, a correct uncertified answer need not be a lucky guess: 142 unchecked threshold answers were information-sufficient but never certified by that policy. This reporting distinction has a retained regression.

See `docs/observation-v1-results.md` and `artifacts/observation_v1.json`.

## 3. Information and feasible-action boundary

Exhausted all **256** binary observation/answer-map combinations on four states: fiber constancy and existence of an observation-only answer map agree in every case (60 sufficient, 196 insufficient).

Exhausted **32,768** three-state relational-contract/observation/feasible-action combinations: intersection construction and independent enumeration agree in every case (7,172 feasible, 25,596 infeasible).

A concrete control has pairwise-overlapping allowable responses `{a,b}`, `{b,c}`, `{a,c}` but no response valid in all indistinguishable worlds. Pairwise overlap alone is insufficient for general contracts. Adding deferral helps only when the contract allows it and the feasible-action set includes it.

These finite checks illustrate standard mathematics. They neither prove a new theorem nor price construction of an informative sensor or compatible-world model. Action sets are formal permissions, not an exercised OS/organizational authorization boundary.

See `docs/protocol-information-v1.md` and `artifacts/information_v1.json`.

## Verification, misses and limitations

- Full repository run: 76 tests, initial `artifacts/situated_v1-full-tests.txt` and final `artifacts/situated_v1-final-tests.txt`. A separately exported pre-change HEAD passed all 43 baseline tests. Pyflakes F checks pass on new Python files; non-strict mypy with skipped imports passes on the six new implementation/runner files.
- Post-run lint removed two unused release-test imports only. Original test source is archived at `artifacts/release_v1-test-source.txt`; new byte-identical `release_v1_verified1/2` receipts match current sources. The audit proves the original/verified receipts differ only in the test-source hash, not fixtures, decisions, costs or any implementation hash.
- Independent post-run audit: `tests/test_situated_receipt_audit.py`; no imports from experiment implementations. Reconstructs received observation state and all its declared counters, recalculates actual/possible-world output conditions, release eligibility, release cost aggregation/exposures, source hashes and repeated receipts.
- Observation and release were independently executed again by the parent and matched the worker receipts byte-for-byte. Information audit has two byte-identical runs.
- Observation worker timed out after writing its implementation/tests/two receipts. Parent recovered and verified them, then wrote its missing results report. Timeout is retained as an operational failure, not represented as worker completion.
- Release targeted tests reported 10 passes; behavioral RED history and exclusions are in its readout. Information tests began with API stubs producing real assertion failures; CLI absence was setup failure, not behavioral proof.
- `correct_not_guaranteed` was initially too easy to read as fortuitous correctness. Observation now separately reports actual evidence sufficiency versus policy certification; retained regression failed before the reporting fix.
- Local freezes are not external preregistration. Input cells share seeds, trajectories and controls: row counts are not independent samples, and reported wins are not confidence estimates.

Release costs are mixed-unit sensitivities; observation costs are listed logical actions. Neither is measured runtime, dollars or energy. Serialization CPU, allocations, context discovery, key lifecycle, real network reliability/latency and human validation remain uncalibrated/excluded. Shared evidence is an attestation relying on issuer correctness; its HMAC uses a public laboratory key and supplies no real deployed security. Observation checkpoints assume all writes participate in atomic logging; unlogged bypass writes and checkpoint loss remain outside the guarantee.

## Reproduce locally

Fresh paths required:

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 scripts/run_observation.py --output artifacts/observation_v1-local.json
PYTHONPATH=src python3 scripts/run_release.py --prefix artifacts/release_v1_local
PYTHONPATH=src python3 scripts/run_information.py --output artifacts/information_v1-local.json --summary artifacts/information_v1-local-summary.md
```

No dependencies installed, no network actions or publication. Before extending synthetic dimensions, the useful next empirical step is to calibrate real validation/evidence/transport costs for a specific application. Current results already show both the mechanism and its failure boundary; another favorable invented price table would not strengthen them.
