# History applicability: executed readout and interpretation

HISTORICAL v1 COSTS: superseded after reviewer found undercounted total reads/writes. Current quantitative results: docs/history-v1.1-results.md and artifacts/history_v1_1.json. Inputs and correctness outcomes unchanged; three feed-repair cost rankings reverse. The old receipt/source commit remains preserved.

## What was tested

Result/intermediate-state history, not trained AI policies: each task returns a vector of shared subproblem sums of squares, its total, and a threshold decision. Inputs change over time. Compare cold recomputation, checked incremental repair, unchecked reuse, and event-feed-driven repair. Frozen protocol: docs/protocol-history-v1.md. Full data: artifacts/history_v1.json. Generated tables: artifacts/history_v1-summary.md.

48 cells represent 24 configured trajectories (16 distinct world hashes), each replayed with a complete or omitted-event feed. Each has initialization plus 32 updates and four policies. Sizes 16 and 64; three seeds; no changes, one changed input, one quarter changed, and all changed. These are controlled fixtures, not sampled real workload distributions. Full-update and no-update trajectories do not gain independent diversity from the three seeds.

## Main equal-correctness comparison

Representative n=64, seed=1, costs include initial setup:

| Changes per update | Cold recomputation | Full-snapshot repair | Unchecked reuse | Unchecked wrong outputs |
|---|---:|---:|---:|---:|
| 0 | 40,161 | 8,065 | 1,249 | 0 |
| 1 | 40,161 | 11,169 | 1,249 | 32 |
| 16 | 40,161 | 43,803 | 1,249 | 32 |
| 64 | 40,161 | 71,553 | 1,249 | 24 |

All numbers are sums of LISTED UNIT-WEIGHT OPERATION COUNTERS, not runtime, dollars, energy or calibrated equivalent work. Counter vectors are retained. Cold and snapshot returned exact results at every step. At sparse change snapshot used less counted work; at quarter/full changes it used more. That direction held at both sizes and across all tested seeds. No universal crossover value follows.

The no-change case matters: unchecked reuse is correct and cheapest in this trajectory, despite performing no maintenance. Thus this does NOT establish that history maintenance must always have positive per-use cost. The full-change stale cache becomes correct again every fourth update because inputs cycle modulo four; there are 24 erroneous updates, not 32. Semantic validity is not identical to a version mismatch.

## Applicability depends on observation guarantees

With one change per step, complete-feed repair uses 5,121 units and stays exact. With odd-index changes omitted it uses 3,421 but returns 32 wrong outputs. Full-snapshot repair remains exact under both feeds. The feed policy computes from its own cache only; truth input is not read during feed repair. Feed production, transport and authentication are not measured or charged. Its advantage is conditional on the availability of an inexpensive complete feed, not an end-to-end victory over scanning.

Across omitted-feed cells: feed repair has 522 wrong outputs, including 49 false acceptance decisions. Cold and snapshot have zero. Do not treat these as population probabilities. The omission mechanism deliberately hides all odd-index changes, starts their cached values at zero, and never refreshes them; in this construction it biases totals downward. The absence of false rejections is fixture-specific, not a generic property of stale caches.

For the n=64, seed=1, one-change trajectory, stale outputs do NOT flip the threshold decision. They still violate the full-vector/total contract. Pricing these errors as consequential depends on the task. If only the Boolean decision mattered, the error/loss surface would be different. The contract is part of the cost problem, not decorative metadata.

## Explicit consequence prices, not free correctness relaxation

Report J = counted operations + lambda * wrong-output-count, as specified BEFORE the run. Lambda is a hypothetical penalty in the same proxy units. Errors are deterministically observed; no invented probability of downstream loss is used. Wrong output, false acceptance and false rejection remain separate fields.

At penalty zero, unchecked wins all 48 cells. At 10,000 per wrong output, unchecked wins only the 12 no-change cells; other cells select exact policies in this grid. This is a conditional utility comparison, NOT a claim that unsafe reuse is acceptable for production.

For n=64/seed=1/one-change with omitted feed, snapshot is the cheaper observed-exact method. Unchecked breaks even against it at penalty 310 per wrong output. With complete feed, the cheaper exact comparator is feed repair and the unchecked threshold is 121. These are exact fixture prices, not measured costs of failure. Choosing the policy from hindsight requires outcomes unavailable to a live selector; no free adaptive optimizer is claimed.

## The revised principle

Prior computation can change future cost. Reuse depends on applicability assumptions; establishing or maintaining those assumptions may cost work, consume information access, or leave residual error.

Distinguish four histories: cached answers, intermediate state/indexes, models of the environment, and decision policies. This run tests the first two. The previous gate experiment shows a policy order can lose its advantage after workload change; it does not implement a trained/adaptive selector.

For learned ordering, optimize only over admissible policies that respect prerequisites and acceptance requirements. An unconstrained argmin can 'win' by skipping verification. Expected loss and correctness constraints are separate choices. D_t changing does not imply the optimal policy must change; it removes the guarantee of stability.

A validation policy may itself need applicability checking, but this does not entail infinite recursive checking. A bounded system needs declared assumptions, monitored failure conditions, resource limits and explicit authorization boundaries. Do not double-count maintenance if C(P|H) already includes checking H.

## Verification

- Protocol and SHA-256 frozen before implementation.
- Initial tests failed with missing history module; not claimed as individual behavioral RED coverage.
- Primary suite: 38 tests passed in 2.901 seconds. Post-run adversarial properties then added arbitrary replacements and partial-feed cache isolation, without changing the frozen primary cases or source files. Final suite: 40 tests passed in 3.143 seconds. The added audit tests are in tests/test_history_properties.py and are outside the original receipt's source manifest.
- Two retained receipts and two summaries byte-identical.
- Independent audit recomputed oracle values using a different indexing loop, checked 6,336 policy-step decisions, source hashes, counter sums, consequence prices, winners, and paired world identities.
- Tests cover shared invalidation/deduplication, hidden change with unchanged feed, aggregate equality despite vector mismatch, exact initial cost counters, zero-change behavior, complete-feed correctness, CLI readback and overwrite refusal.
- Source/code review subsequently completed: four findings resolved in docs/history-v1.1-results.md. Original numbers below/above are retained as the v1 record, not current cost claims.
- No dependencies installed, external calls, publication, permission changes, or physical interventions.

## Limits that could change the decision surface

Listed counters exclude loop control, allocation, fixed dependency generation, feed production, world generation, oracle work and output serialization. The graph and arity are fixed; only values drift. Dynamic dependency edges, concurrency, races, delayed/reordered/forged feeds, crash recovery and learned repair policies are untested. Unit weights can move the apparent crossover; physical calibration is needed before engineering deployment claims. The subproblem function has exploitable algebra and this is not an optimal solver comparison. Do not infer difficulty of arbitrary repeated search from incremental maintenance of these sums.
