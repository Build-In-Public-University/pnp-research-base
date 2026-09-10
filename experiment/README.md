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
- Dense-coupling calibration v1: measured multi-input join and reverse-index costs; results in `docs/dense-coupling-v1-results.md`.
- Overlapping-updates calibration v1: measured union versus summed invalidation sets; results in `docs/overlapping-updates-v1-results.md`.
- Semantic-interaction calibration v1: explicit joint-constraint counterexample to fixed-union repair; results in `docs/semantic-interaction-v1-results.md`.
- Archive-transition calibration v1: application-specific state-versus-transition interaction; results in `docs/archive-transition-interaction-v1-results.md`.
- Archive release-contract calibration v1: actual manifest validation with a transition-aware migration rule; results in `docs/archive-release-contract-v1-results.md`.
- History-sufficiency calibration v1: theorem witness and retained-state comparison; results in `docs/history-sufficiency-v1-results.md`.
- Recursive history-sufficiency calibration v1: decision, update, and continuation factorization; results in `docs/recursive-history-sufficiency-v1-results.md`.
- Contract-relative state complexity v1: future-equivalence classes and lifecycle cost tuple; results in `docs/contract-relative-state-complexity-v1-results.md`.
- Parameterized contract-state scaling v1: `K_G(n)`, semantic bits, distinguishing depth, and lifecycle axes; results in `docs/parameterized-contract-state-scaling-v1-results.md`.
- Fixed-contract architecture calibration v1: raw mask, materialized count, sparse set, and event-log tradeoffs; results in `docs/fixed-contract-architecture-v1-results.md`.
- Physical fixed-contract architecture benchmark v1: local wall/CPU timing, allocation proxy, and logical I/O across size/workload ratios; results in `docs/physical-architecture-benchmark-v1-results.md`.
- Interactive observation-policy calibration v1: passive versus privileged/active energy identifiability under different authorized observation actions; results in `docs/interactive-observation-policy-v1-results.md`.
- Adaptive observation-policy calibration v1: finite policy search for the minimum-cost sufficient channel composition; results in `docs/adaptive-observation-policy-v1-results.md`.
- Branching adaptive observation-policy calibration v1: conditional stop/escalate policy with expected versus worst-case observation cost; results in `docs/branching-adaptive-observation-policy-v1-results.md`.
- Loss-aware adaptive observation calibration v1: finite-loss stop-versus-observe decisions under common and rare residual risk; results in `docs/loss-aware-observation-v1-results.md`.
- Dual-control observation/action calibration v1: compare immediate action, non-destructive inspection, and an informative intervention; results in `docs/dual-control-observation-action-v1-results.md`.
- Dual-control policy phase diagram v1: sweep the fragile-state prior and verify the act/experiment/inspect/act policy regions; results in `docs/dual-control-policy-phase-diagram-v1-results.md`.
- Action-relative value-of-information calibration v1: equal-entropy beliefs with different optimal policies under asymmetric intervention costs; results in `docs/action-relative-voi-v1-results.md`.
- Capability-space routing calibration v1: discover, move, connect, transfer, and compose capabilities across nodes; results in `docs/capability-space-routing-v1-results.md`.
- Persistent capability reuse calibration v1: compare fresh discovery, retained remote routes, and local replication under repeated demand; results in `docs/persistent-capability-reuse-v1-results.md`.
- Capability placement freshness calibration v1: add change-rate-dependent refresh/validation costs to the demand surface; results in `docs/capability-placement-freshness-v1-results.md`.
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

Dense coupling is now measured too. Across 30 cells, full edge checks were
`12, 24, 48` for join widths `1, 2, 4`, while incremental checks were
`fan-out × join width`; all results were mechanically exact. This exposes the
approach to \(\rho=1\) without turning local timing into a universal claim.

Overlapping updates are measured separately. Across 24 cells, disjoint changes
had zero overlap savings, while adjacent/clustered changes saved up to 9 repair
records when join width was 4. Every indexed result remained mechanically exact.
Repair scope followed the union of affected sets, not their isolated sum.

Semantic interaction is measured separately. In 12 cells, ordinary union repair
was exact in the disjoint/adjacent controls but missed one explicit joint
constraint in every joint/cluster cell. Interaction-aware repair restored
exactness. This is a synthetic counterexample to fixed-union sufficiency, not a
claim about inferred real-world semantics.

The archive/release transition calibration separates missing state indexing from
transition-relative semantics. Isolated manifest or compatibility changes are
handled by singleton and state-complete repair. A simultaneous change activates
an explicit `migration-approval` artifact that only transition-aware repair
captures. The result is application-specific and bounded to the frozen release
contract.

The release-contract calibration uses the actual repository manifest and checks
file presence, byte counts, and SHA-256 digests. Manifest-only and
compatibility-only releases pass state checking. A simultaneous change passes
the current-state checker but fails the independent transition oracle without
`migration-approval`; the bound receipt restores validity. The migration rule
migration requirement is a newly declared research protocol, not existing production policy.

History sufficiency is measured next. Two release histories share the same
current-state representation but have different contract outcomes. `current_only`
is therefore an exactness impossibility witness; event-log, transition-record,
trusted-digest, and minimal contract-state representations distinguish the pair.
The compact forms are trusted controls, not self-authenticating proofs.

The recursive calibration turns the contract into a finite state machine with
`clean`, `migration_missing`, and `migration_satisfied` states. Observation and
update both factor through that state; exhaustive continuations through length
6 pass (19,531 sequences), and induction supplies the all-finite-continuation
claim. A trusted one-byte state code distinguishes the three semantic states;
byte size is not an authenticity guarantee.

Contract-relative state complexity is measured over the same finite machine.
There are three reachable, pairwise future-distinguishable classes, so
`K_G=3` and the ideal fixed-length semantic requirement is two bits. The
receipt separates retained bytes from modeled observation, update, decision,
and evidence counters; these are not wall-clock benchmarks.

The parameterized mask family separates state count from state information and
operational cost: `K_G(n)=2^n`, `I_G(n)=n`, one-bit modeled updates, and n-bit
decision scans. Maximum distinguishing depth is n in this family. These are
exact family results and modeled costs, not universal asymptotic claims.

The fixed-contract architecture calibration holds `G_n` constant while varying
representation. A raw mask scans n bits; a mask plus unresolved-count index
keeps the same semantic mask but makes the global query constant-time; a sparse
set changes physical representation; and an event log shifts work to replay.
All four remain oracle-exact. The result is a resource vector, not a universal
ranking.

The physical benchmark measures the same four architectures at `n = 128, 512,
2048, 8192` and query/update ratios `0.1, 1, 10, 100`. It records local wall and
CPU time, tracemalloc peak allocation, instrumented logical I/O, and exactness.
At `n=8192, r=100`, raw/counter/sparse/event-log wall medians were 30.0 ms,
14.8 ms, 14.3 ms, and 661.7 ms. At `n=128, r=0.1`, they were 9.9, 14.3, 4.9,
and 6.5 microseconds. This is a local calibration, not an energy measurement
or universal crossover; no package-power counter was used.

The interactive observation-policy calibration makes the measurement boundary
explicit. Two synthetic hidden states have identical ordinary observations but
different energy labels. Passive transcripts cannot identify energy; privileged
telemetry and active calibration can, at modeled observation cost and with
measurement perturbation. This is a structural synthetic result, not an energy
measurement.

The adaptive observation calibration holds a four-state exact-identification
contract fixed while composing complementary channels. Either coarse channel
alone is insufficient; `local_group -> local_parity` identifies all states at
modeled cost 4, while `privileged_exact` costs 6. This is a bounded finite
policy result, not a general optimal decision-tree solver.

The branching adaptive calibration adds conditional stopping and escalation.
Two states resolve after the first cheap observation, two after a second local
observation, and one requires privileged telemetry. The policy is exact with
worst-case modeled cost 9 and uniform-prior expected cost 3.4, versus cost 6
for always using privileged telemetry. Expected and worst-case observation
costs are therefore kept separate.

The loss-aware observation calibration adds finite wrong-decision loss. In the
common/high-loss scenario, residual risk 0.5 produces stop risk 10, so the
policy buys privileged observation at cost 6. In the rare/low-loss scenario,
residual risk 0.1 produces stop risk 2, so the policy acts safely without
resolving the final state ambiguity. Expected costs are 4.6 and 1.06. This is
a synthetic stopping-policy result, not hardware energy telemetry.

The dual-control calibration makes an action epistemic as well as
interventional. A gentle touch reveals the hidden state but can damage a
fragile object. At fragile prior 0.1 it is preferred (modeled cost 3 versus 6
for inspection); at prior 0.5, non-destructive inspection is preferred (6
versus 7). This is synthetic modeled cost, not a physical risk measurement.

The dual-control phase diagram sweeps the fragile-state prior at resolution
0.001. The lower envelope is immediate action through 0.011, gentle touch
from 0.012 to 0.399, inspection from 0.4 to 0.95, and immediate action again
from 0.951 onward. The analytic crossings are 1/90, 0.4, and 0.95. This is a
synthetic modeled-cost phase diagram.

The action-relative value-of-information calibration compares p=0.1 and p=0.9.
They have equal binary entropy and equal perfect-information risk reduction,
but different touch costs because intervention risk is state-asymmetric. Touch
is optimal at p=0.1; inspection is optimal at p=0.9. Entropy alone therefore
does not determine the rational attention policy.

The capability-space routing calibration promotes reachable capabilities into
the state. Starting at node `i` with `{parity}`, the least-cost route to the
contract `{parity, group}` is `discover -> move -> connect -> transfer ->
compose`, with modeled cost 11. Discovery changes capability knowledge;
transfer changes the reachable capability set; composition closes the
contract.

```bash
PYTHONPATH=src python3 scripts/run_capability_space_routing_v1.py \
  --output artifacts/capability_space_routing_v1-local.json \
  --summary artifacts/capability_space_routing_v1-local.md
```

```bash
PYTHONPATH=src python3 scripts/run_action_relative_voi_v1.py \
  --output artifacts/action_relative_voi_v1-local.json \
  --summary artifacts/action_relative_voi_v1-local.md
```

```bash
PYTHONPATH=src python3 scripts/run_dual_control_policy_phase_diagram_v1.py \
  --output artifacts/dual_control_policy_phase_diagram_v1-local.json \
  --summary artifacts/dual_control_policy_phase_diagram_v1-local.md
```

```bash
PYTHONPATH=src python3 scripts/run_dual_control_observation_action_v1.py \
  --output artifacts/dual_control_observation_action_v1-local.json \
  --summary artifacts/dual_control_observation_action_v1-local.md
```

```bash
PYTHONPATH=src python3 scripts/run_loss_aware_observation_v1.py \
  --output artifacts/loss_aware_observation_v1-local.json \
  --summary artifacts/loss_aware_observation_v1-local.md
```

```bash
PYTHONPATH=src python3 scripts/run_branching_adaptive_observation_policy_v1.py \
  --output artifacts/branching_adaptive_observation_policy_v1-local.json \
  --summary artifacts/branching_adaptive_observation_policy_v1-local.md
```

```bash
PYTHONPATH=src python3 scripts/run_adaptive_observation_policy_v1.py \
  --output artifacts/adaptive_observation_policy_v1-local.json \
  --summary artifacts/adaptive_observation_policy_v1-local.md
```

```bash
PYTHONPATH=src python3 scripts/run_interactive_observation_policy_v1.py \
  --output artifacts/interactive_observation_policy_v1-local.json \
  --summary artifacts/interactive_observation_policy_v1-local.md
```

```bash
PYTHONPATH=src python3 scripts/run_physical_architecture_benchmark_v1.py \
  --output artifacts/physical_architecture_benchmark_v1-local.json \
  --summary artifacts/physical_architecture_benchmark_v1-local.md
```

```bash
PYTHONPATH=src python3 scripts/run_fixed_contract_architecture_v1.py \
  --output artifacts/fixed_contract_architecture_v1-local.json \
  --summary artifacts/fixed_contract_architecture_v1-local.md
```

```bash
PYTHONPATH=src python3 scripts/run_parameterized_state_scaling_v1.py \
  --output artifacts/parameterized_state_scaling_v1-local.json \
  --summary artifacts/parameterized_state_scaling_v1-local.md
```

```bash
PYTHONPATH=src python3 scripts/run_contract_complexity_v1.py \
  --output artifacts/contract_complexity_v1-local.json \
  --summary artifacts/contract_complexity_v1-local.md
```

```bash
PYTHONPATH=src python3 scripts/run_recursive_history_v1.py \
  --output artifacts/recursive_history_v1-local.json \
  --summary artifacts/recursive_history_v1-local.md
```

```bash
PYTHONPATH=src python3 scripts/run_history_sufficiency_v1.py \
  --output artifacts/history_sufficiency_v1-local.json \
  --summary artifacts/history_sufficiency_v1-local.md
```

```bash
PYTHONPATH=src python3 scripts/run_archive_release_contract_v1.py \
  --output artifacts/archive_release_contract_v1-local.json \
  --summary artifacts/archive_release_contract_v1-local.md
```

```bash
PYTHONPATH=src python3 scripts/run_archive_transition_v1.py \
  --output artifacts/archive_transition_v1-local.json \
  --summary artifacts/archive_transition_v1-local.md
```

```bash
PYTHONPATH=src python3 scripts/run_interaction_v1.py \
  --output artifacts/interaction_v1-local.json \
  --summary artifacts/interaction_v1-local.md
```

```bash
PYTHONPATH=src python3 scripts/run_overlap_v1.py \
  --output artifacts/overlap_v1-local.json \
  --summary artifacts/overlap_v1-local.md
```

```bash
PYTHONPATH=src python3 scripts/run_dense_coupling_v1.py \
  --output artifacts/dense_coupling_v1-local.json \
  --summary artifacts/dense_coupling_v1-local.md
```

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
