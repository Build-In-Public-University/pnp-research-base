# P vs NP as a Network-Architecture Problem

This repository attacks a narrow research thesis:

> Standard P and NP are defined relative to a formal computational model, but the operational cost of solving, validating, transporting, reproducing, and maintaining a result is architecture-relative.

The repository is deliberately adversarial. It must be able to show that the thesis is weak, tautological, or merely a relabeling of runtime.

## Status

- v2: executed, bounded synthetic algorithm experiments, not a complexity-theoretic result.
- Dynamic dependency repair v1: executed, bounded synthetic repair/invalidation experiment; results in `docs/dynamic-v1-results.md`.
- Dynamic dependency consequence v2: executed, bounded synthetic delayed-validation and stale-consequence experiment; results in `docs/dynamic-v2-results.md`.
- Concrete calibration v1: measured local archive-manifest integrity replay; results in `docs/calibration-v1-results.md`.
- Fan-out calibration v1: measured dependency geometry over layered archive-derived records; results in `docs/fanout-v1-results.md`.
- Explicit graphs, message traversal, submitted-witness checks and actual 3-CNF enumeration.
- Frozen specification: `docs/protocol-v2.md` and `docs/protocol-v2.sha256`.
- Results: `artifacts/experiments_v2.json`; readable summary: `artifacts/experiments_v2-summary.md`.
- No real parallel hardware or deployed validation service. Public archive publication is separate from experimental validity.

## Latest: dynamic dependency repair

`docs/dynamic-v1-results.md` records the next hard gate: recomputation versus
selective repair, full reset, certificate validation and unchecked reuse under
state churn, dependency-edge churn and hidden drift. The 144-cell sweep found
47 wrong outputs for visible selective repair and 47 for visible full reset when
the dependency change was hidden; certificate repair returned zero wrong outputs
but had higher modeled operation cost than cold recomputation in this fixture.
The unchecked control returned 1,044 wrong outputs. These are finite synthetic
results, not runtime or P/NP evidence.

## Latest: consequence-aware validation

`docs/dynamic-v2-results.md` extends v1 with partial/delayed certificate
availability and deterministic downstream consequences for stale reuse. Across
288 cells, complete certificate repair had zero wrong outputs; delayed
certificates had 293; visible selective repair had 766; unchecked reuse had
2,088. At zero consequence penalty, unchecked reuse was cheapest; at penalty
1,000, certificate repair won 96 cells and delayed validation won 50. These are
fixture-specific modeled costs, not incident probabilities or deployment data.

```bash
PYTHONPATH=src python3 scripts/run_dynamic_v2.py \
  --output artifacts/dynamic_v2-local.json \
  --summary artifacts/dynamic_v2-local.md
```

```bash
PYTHONPATH=src python3 scripts/run_dynamic.py \
  --output artifacts/dynamic_v1-local.json \
  --summary artifacts/dynamic_v1-local.md
```

## Latest: observation, information and staged release

**76 tests passing.** Combined readout: [`docs/situated-v1-results.md`](docs/situated-v1-results.md).

- [Observation systems](docs/observation-v1-results.md): 6,144 policy-tick decisions; source logging, checkpoints, acquisition and recovery now charged. Sparse logging wins, dense logging loses, event loss can reverse a win. Safe abstention is not full service.
- [Staged release](docs/release-v1-results.md): 78,240 safe candidate-recipient decisions match the oracle. Shared trusted attestations eliminate duplicate checks but can lose after byte costs. Local applicability and issuer correctness remain necessary.
- [Information boundary](artifacts/information_v1-summary.md): exhaustive finite observation/contract/feasible-action checks; standard mathematics, not a new complexity theorem.

New protocols and receipts are separate from history v1.1. Observation and release each have two worker receipts plus a byte-identical independently executed parent run. No real deployment or network publication occurred.

```bash
# Fresh paths required for each invocation.
PYTHONPATH=src python3 scripts/run_observation.py --output artifacts/observation_v1-local.json
PYTHONPATH=src python3 scripts/run_release.py --prefix artifacts/release_v1_local
PYTHONPATH=src python3 scripts/run_information.py \
  --output artifacts/information_v1-local.json --summary artifacts/information_v1-local-summary.md
```

## First attack (historical, arithmetic-only)

The old `model.py` and preserved `artifacts/first_attack.json` are **arithmetic-only parameter-bundle bookkeeping**. The named graphs were not edge sets. `local_verify_ops = input_length + certificate_length` was an assumed cost, **not an executed certificate verifier**. Those outputs do not demonstrate SAT verification, propagation, or global consistency.

## Run

From the repository root, using only Python's standard library:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v

# Use fresh paths: the v2 runner refuses to overwrite existing artifacts.
PYTHONPATH=src python3 scripts/run_experiments_v2.py \
  --output artifacts/experiments_v2-local.json \
  --summary artifacts/experiments_v2-local-summary.md
PYTHONPATH=src python3 scripts/run_experiments_v2.py \
  --output artifacts/experiments_v2-local-repeat.json \
  --summary artifacts/experiments_v2-local-repeat-summary.md
cmp artifacts/experiments_v2-local.json artifacts/experiments_v2-local-repeat.json
cmp artifacts/experiments_v2-local-summary.md artifacts/experiments_v2-local-repeat-summary.md

# Legacy arithmetic-only fixture, without overwriting its historical receipt:
PYTHONPATH=src python3 -m pnp_architecture.cli --output /tmp/pnp-first-attack-local.json
# Equivalent: PYTHONPATH=src python3 scripts/run_attack.py --output /tmp/pnp-first-attack-local.json
```

The v2 receipt embeds input/config identities, explicit edge sets and formulas, exact truth tables, loop counters and source hashes. Its repeat receipt is byte-identical. The test suite independently exercises the runner twice in temporary directories and checks overwrite refusal.

BFS setup inspections, message sends, payload-bit-hops, literal inspections and idealized scheduling makespan are distinct units, not a composite energy or timing score. Disconnected collections report unavailable. Rejected submitted witnesses are not UNSAT claims. CNF makespan is a serially computed scheduling idealization that excludes hardware, communication and formula replication costs; input size includes clauses. Brute-force enumeration establishes no SAT lower bound.

## Third feedback: history, observation, action and gates

`docs/pnp3-integration.md` integrates the third source with explicit corrections:
accessible retained state, observation channels, permitted actions, separate
search/validation effort, and progressive validation. Claims and falsifiers are
in `claims/pnp3.md`. Neither conservation of complexity nor AI-induced
search/validation divergence is established.

The executed gate pilot shows cheap-first is not universally optimal under its
declared synthetic invocation prices; all policies match the same acceptance
oracle. See `docs/gates-v1-results.md` and `artifacts/gates_v1.json`.

```bash
# Fresh output path required; no provider or external actions.
PYTHONPATH=src python3 scripts/run_gates.py --output artifacts/gates_v1-local.json
```

History under changing values in fixed shared dependencies is now executed:
`docs/history-v1.1-results.md`, `artifacts/history_v1_1.json` and its generated summary.
Review corrected undercounted total reads/writes and reversed three feed-repair
cost rankings; historical v1 receipts remain available, not overwritten.
The full-snapshot policy saves listed operation counts with sparse changes but
loses to recomputation with heavier churn. Event-feed repair can silently return
stale results when events are omitted. Consequence prices are synthetic; safety
and cost are reported separately. No result-cache experiment establishes learned
policy adaptation or a general dynamic-search theorem.

```bash
PYTHONPATH=src python3 scripts/run_history.py \
  --output artifacts/history_v1_1-local.json \
  --summary artifacts/history_v1_1-local-summary.md
```

Changing dependency edges and delayed certificate delivery are now executed in
dynamic v1/v2. Calibration against one concrete application, partial delivery
failure, explicit human/downstream consequences, learned policy adaptation and
action-access boundaries remain open. Old v2, gate and history receipts are
unchanged.

The first calibration is now complete for the archive manifest itself. Four
one-file updates over 24 copied files were mechanically exact; full recompute
hashed 96 file instances while indexed repair hashed 4. This is a local
filesystem measurement, not a distributed timing or universal advantage claim.

The fan-out calibration is also complete: 30 cells varied fan-out, graph depth,
and assurance scope. Affected fraction ranged from 0.083 to 0.917, and indexed
repair remained mechanically exact while repair scope followed fan-out × depth.
Full assurance remained separate from affected-only assurance.

```bash
PYTHONPATH=src python3 scripts/run_fanout_v1.py \
  --output artifacts/fanout_v1-local.json \
  --summary artifacts/fanout_v1-local.md
```

```bash
PYTHONPATH=src python3 scripts/run_calibration_v1.py \
  --output artifacts/calibration_v1-local.json \
  --summary artifacts/calibration_v1-local.md
```

## Sources

- Stephen Cook, “The P versus NP Problem,” Clay Mathematics Institute:
  https://www.claymath.org/wp-content/uploads/2022/06/pvsnp.pdf
- Clay overview: https://www.claymath.org/millennium/p-vs-np/
- Working thesis: `docs/pnp-network-architecture-analysis.md`

## Boundaries

This project does not redefine P or NP, claim a proof of P ≠ NP, treat human discovery as NP, or infer universal complexity laws from a synthetic graph. The unit under measurement is a declared system lifecycle, not a language membership decision.
