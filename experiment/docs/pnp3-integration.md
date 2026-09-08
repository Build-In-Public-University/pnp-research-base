# Third feedback integration: state, access, and validation gates

Source: user-supplied `pnp 3.md`, reviewed in full (852 lines). Raw conversation is not copied into the repository. Line ranges below identify provenance. This is a corrected integration, not endorsement of every source claim.

## Revised object

Use a cost VECTOR for an operational task and a particular protocol:

C_t = C(P_t, pi, A, B_t, G_t; H_t, O_t, U_t).

P: task/instance; pi: algorithm/protocol; A: architecture; B: resource budget; G: acceptance predicate; H: accessible retained state; O: observation function/channel; U: permitted actions. Reachable states are derived from current state, transition rules, U, budget and deadline, not an independently assumed capability. Keep costs of discovery, local verification, composition, transport/coordination, setup, maintenance and authority acquisition separate. Resource counters remain vectors unless a calibrated or explicitly modeled price vector is supplied.

This is an operational cost model, not a new definition of P/NP or intelligence. Complexity classes require quantification over algorithms and input families, uniformity, and resource bounds. History must be generated and maintained or declared as advice/side information; it is not a free oracle.

## 1. History and amortization (source lines 35-55, 157-243)

Adopt H as accessible, versioned computational state. Cold versus warm starts differ by available resources, not computational power by fiat. Record setup, lookup, storage occupancy, freshness checks, update detection, invalidation, repair and discarded work. Over a trajectory report setup plus each later component separately. Cached state can save computation; costs need not be conserved.

Existing v2 evidence supports stable-route reuse only. It does NOT measure graph drift, semantic changes, retained human knowledge, or energy. Priority experiment: full recomputation versus incremental repair versus unchecked cache on the SAME ordered changes. Include no changes, sparse changes, dense churn, hidden dependencies, and stale metadata. Require equal correctness; count false acceptance and unresolved states, not merely throughput.

## 2. Observability and action reach (247-480)

Adopt distinct outcomes: solved/validated, insufficient observations, known solution but action unavailable, and exhausted compute budget. An observation is a channel, not necessarily a literal subset of world state. If two states give identical accessible observations but require opposite answers, no deterministic observer can always answer correctly without more information. This is an indistinguishability boundary, not NP-hardness.

A correct answer does not grant permission to act. Keep approval, available tools and external writes separate from truth validation. No experiment here will change external permissions or deploy anything. A model's weights are not an inspectable transcript of training history. Expanded access may help or inject irrelevant or incorrect material; AI does not monotonically expand reliable observation by definition. 'Local spacetime' and 'light cone' remain metaphors unless physical causality is modeled.

## 3. Search versus validation distance (482-695)

Adopt separate metrics for retrieval effort, physical hop count, provenance depth, semantic/version mismatch, independent evidence sources and local reproduction work. Do not subtract quantities with different units as one delta-distance. Do not assume geographical distance predicts validation cost.

The claim that AI flattens retrieval costs while validation costs rise is OPEN, not established by our graphs. A simulation that assigns constant retrieval cost and increasing validation cost builds the divergence into its assumptions. It can test accounting but cannot verify that law.

Required counterexamples: distant proof-carrying answer checked locally; direct access to the original source bypassing intermediate summaries; many apparent corroborations sharing one origin; a local measurement with a biased or broken instrument; inaccessible source where validation is unavailable rather than assigned a huge cost. Signed provenance establishes origin/integrity, not truth. A repeated source is not independent evidence. No uncalibrated confidence threshold or exp(-lambda*d) trust score will authorize acceptance.

The ratio of validation cost to total knowledge cost can rise even if absolute validation cost is unchanged or falling. Report both. Conditional prediction: if generation arrival rate exceeds validation service capacity, backlog grows absent filtering or capacity changes. This is a queueing condition, not proof of an AI-specific law.

## 4. Progressive gates and consequences (697-851)

Adopt progressive validation as a sequential decision mechanism. Correct the source: later mandatory checks run on candidates that PASS earlier gates; early rejection avoids later cost. Cheap gates need not precede selective gates if dependencies permit reordering.

Expected gate cost is sum_i c_i * Pr(all preceding gates pass). If q_i is CONDITIONAL pass probability at gate i given earlier passes, the equivalent expression is c_1 + q_1*c_2 + q_1*q_2*c_3 + ... . If p_i already means probability of reaching gate i, multiply c_i by p_i once; the source mixes these definitions.

For two independent, reorderable checks with fixed cost c and rejection probability r, i before j costs c_i + (1-r_i)c_j. Thus prefer i before j iff c_i*r_j <= c_j*r_i (cost per rejection, with never-rejecting checks last). With dependence, use conditional rates at the current stage; with prerequisites, evaluate only legal orders. A global best-order benchmark with full outcomes is an oracle reference, not a free online optimizer.

All required gates must pass before acceptance. No cheap-gate shortcut may masquerade as full validation. Gate false negatives/positives, correlated errors, caching and workload drift need separate tests. Human authorization remains a separate boundary after technical validation.

The source's uncertainty*blast-radius*irreversibility expression is a heuristic, not a derived proportionality. Use a declared expected-loss model and safety constraints if pricing failure; retain the risk distribution and price sensitivity. Production actions are not uniformly irreversible, and staging actions are not uniformly harmless. 'Energy' requires physical measurements, not gate cost points.

## Corrections to the overarching rhetoric

- Routing does not prove complexity was conserved or relocated: sends and BFS inspections differ in units; a known star route or non-redundant protocol may avoid both costs. Our BFS scanned every adjacency, but this is not a lower bound on all route construction.
- Time down does NOT imply work up universally. The v2 UNSAT enumeration schedules had equal work across processor counts. Better algorithms can reduce both.
- The achievable set of resource tuples is not itself a Pareto frontier; its nondominated subset is. A frontier over three tested schedules is a sampled frontier, not all possible architectures.
- Local validity not implying global composition is established for our fixture. The composition task itself remains polynomial.
- Retained state, observation and authority are distinct; none turns a standard language from P into NP.

## Subsequent execution update

The fixed-dependency, changing-value history experiment has since run. See
`docs/history-v1.1-results.md`: sparse snapshot repair beats cold recomputation in
listed unit-cost counters; quarter/full churn reverses that ordering. Complete
feed repair stays exact; omitted-feed repair can become stale. No-change reuse
is a correct low-cost control, so nonzero per-use maintenance is not universal.
The priority list below records the integration-stage sequence, not current completion.

## Integration status and next artifacts

1. Defined: expanded operational model above; source claims corrected.
2. Executable now: bounded deterministic gate-order pilot, docs/protocol-gates-v1.md and artifacts/gates_v1.json. Costs are declared model units; acceptance uses real predicates.
3. Next: repeated solving with versioned shared dependencies, equal-correctness controls and charged maintenance.
4. Then: observation/action boundary fixtures with paired indistinguishable states and explicit denied-action outcomes.
5. Later, separately authorized: real retrieval/provider calibration for search-validation divergence. No human/AI benefit claim from a hard-coded curve.

No novelty claim until related work in amortized/dynamic algorithms, distributed verification, communication complexity, partial observability, sequential testing and incremental computation is examined from primary sources.
