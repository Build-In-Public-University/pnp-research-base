# Claim readout after executed v2 experiments

Evidence: artifacts/experiments_v2.json and its byte-identical repeat; independent parent execution in artifacts/experiments_v2-parent.json has identical graph, propagation, containing-constraint, and CNF outputs and source hashes. Status: executed finite synthetic algorithms, not real distributed hardware or novel complexity evidence.

## Outcomes

1. Topology-only explanation is insufficient. At N=32, complete-graph flooding uses 992 sends and star flooding 62. Routed propagation uses 31 sends on either; BFS setup costs 992 versus 62 adjacency inspections. The algorithm can remove a traffic difference without changing physical connectivity. Chain/star/tree all route in 31 sends but need 31/1/5 delivery rounds. Work and depth differ; do not sum setup inspections and messages as if they were a calibrated energy unit.
2. Local certificate validity does not authorize global acceptance. The naive rule makes 25 wrong global predictions in 60 deliberately constructed witnesses. The collector accepts 30, rejects 20, abstains on 10 unreachable cases, and has no oracle disagreement on available cases. This is a controlled counterexample, not an error-rate estimate for real networks. All these equality problems are satisfiable; witness rejection is not UNSAT.
3. All 90 search schedules match exhaustive truth tables. The 30 CNF formulas comprise 10 SAT and 20 UNSAT. On each SAT formula, full parallel batching spends more search work than sequential stopping. For n=12, replicate 0: p=1 uses 2,196 literal inspections and idealized span 2,196; p=12 uses 2,248 and span 383; p=4,096 uses 55,323 and span 83. Latency reduction is not work reduction. Actual hardware, input distribution, orchestration, and energy are not measured.
4. Independent tiny logical test: each of all eight signed clauses on three variables has seven local witnesses, but their conjunction has zero. The distinction is between 'for every clause there exists a witness' and 'there exists a witness for all clauses.' An additional test verifies that conflicting submitted local witnesses can also occur in a satisfiable formula.

## What survives

Cost depends jointly on the problem, algorithm/protocol, architecture, resource budget, and acceptance requirement. A local solution may not meet the containing problem's global constraint. Repeated use can amortize a cached route's setup work; this remains a stable-graph reuse experiment, not a drift or recovery experiment.

## What does not follow

- No P/NP class membership changed.
- No energy conservation law or universal complexity migration theorem was established.
- The equality collector is polynomial; it does not demonstrate irreducible exponential global consistency.
- A deliberately wasteful algorithm cannot establish a lower bound for a problem or architecture class.
- Here payload size is varied independently from network size, but this is not evidence of a nontrivial interaction between semantic problem difficulty and network topology.
- Root-centered star and complete graphs are favorable placements; arbitrary-root and congestion experiments remain open.

## Next hard gate

To test repeated solving rather than repeated delivery, introduce changing shared variables across coupled subproblems and compare recomputation, incremental repair, and cached-certificate validation with explicit invalidation and stale acceptance checks. Charge discovery, graph construction, index maintenance, updates, certificate validation and transport separately. Test whether benefits disappear with churn or hidden dependencies. Do not claim novelty until comparing against incremental algorithms, distributed verification, communication complexity and dynamic constraint satisfaction literature.

## Verification

Parent read code and independently checked send-count identities, equal routed/flood delivery depth, and every possible single-conflict location across graph sizes. Full suite: 22 tests passed. Receipt source hashes matched the current files. Original arithmetic receipt retained unchanged and downgraded in claims/ledger.json. Module CLI failure was reproduced, then fixed and covered by a fresh-file test.
