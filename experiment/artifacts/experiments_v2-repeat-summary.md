# Executed bounded experiments v2

Generated from the deterministic JSON receipt; synthetic algorithms only.
Frozen protocol SHA-256: `6976a672e64d772b1e11330d4645f5fa613f0ec3d1e07e38a246a654d8aca987`

Rows: 30 explicit graphs, 120 propagation cells, 60 containing witnesses, 30 CNF formulas.

## Propagation: N=32, payload=64 bits, one use

| Topology | Flood sends | Flood rounds | Tree sends | Tree rounds | BFS inspections | All reached |
|---|---:|---:|---:|---:|---:|---|
| chain | 62 | 32 | 31 | 31 | 62 | True |
| star | 62 | 2 | 31 | 1 | 62 | True |
| balanced_tree | 62 | 6 | 31 | 5 | 62 | True |
| complete | 992 | 2 | 31 | 1 | 992 | True |
| disconnected | 30 | 16 | 15 | 15 | 30 | False |

Sends are measured loop events; bit-hops count payload bits on each hop. Flood rounds
include redundant final transmissions. Routing eliminates dense redundant sends, not setup
inspections or depth. Connected tree routes tie in send counts, a useful negative result.
Reuse totals execute each repetition; setup is charged once, separately, not added to messages.

## Containing constraint

Naive local-only false global predictions: 25.
Centralized accepted/rejected/unavailable: 30/20/10.
Available centralized/oracle disagreements: 0.
All containing problems remain satisfiable; rejections concern submitted witnesses.
Singleton single-one inputs are consistent. Disconnected non-singletons are unavailable.

## CNF: individual n=12 runs (all sizes and full truth tables in JSON)

| Variant | Replicate | Clauses | Satisfying assignments | p | Candidates | Work | Idealized makespan |
|---|---:|---:|---:|---:|---:|---:|---:|
| random | 0 | 48 | 26 | 1 | 163 | 2196 | 2196 |
| random | 0 | 48 | 26 | 12 | 168 | 2248 | 383 |
| random | 0 | 48 | 26 | 4096 | 4096 | 55323 | 83 |
| random_plus_unsat_core | 0 | 56 | 0 | 1 | 4096 | 55575 | 55575 |
| random_plus_unsat_core | 0 | 56 | 0 | 12 | 4096 | 55575 | 10786 |
| random_plus_unsat_core | 0 | 56 | 0 | 4096 | 4096 | 55575 | 92 |
| random | 1 | 48 | 13 | 1 | 321 | 4950 | 4950 |
| random | 1 | 48 | 13 | 12 | 324 | 4982 | 899 |
| random | 1 | 48 | 13 | 4096 | 4096 | 56953 | 87 |
| random_plus_unsat_core | 1 | 56 | 0 | 1 | 4096 | 57096 | 57096 |
| random_plus_unsat_core | 1 | 56 | 0 | 12 | 4096 | 57096 | 10402 |
| random_plus_unsat_core | 1 | 56 | 0 | 4096 | 4096 | 57096 | 97 |
| random | 2 | 48 | 10 | 1 | 1883 | 26584 | 26584 |
| random | 2 | 48 | 10 | 12 | 1884 | 26657 | 4674 |
| random | 2 | 48 | 10 | 4096 | 4096 | 55794 | 82 |
| random_plus_unsat_core | 2 | 56 | 0 | 1 | 4096 | 55900 | 55900 |
| random_plus_unsat_core | 2 | 56 | 0 | 12 | 4096 | 55900 | 10299 |
| random_plus_unsat_core | 2 | 56 | 0 | 4096 | 4096 | 55900 | 90 |

SAT formulas: 10; UNSAT formulas: 20.
SAT formulas where p=2**n uses more work than p=1: 10.
Every schedule matched the independent exhaustive truth table and accounting checks.
All candidates in the winning batch were charged, including candidates after first success.
Large processor budgets trade idealized depth for work; this is not a faster hardware measurement.

## Limitations

- Finite synthetic graphs/formulas only; no universal or P/NP separation claims.
- No real parallel hardware used; makespan is idealized literal-inspection scheduling.
- No real timing, energy, contention, headers, failures, graph generation or memory costs.
- BFS is centralized setup; its adjacency inspections are not network message counts.
- CNF search excludes assignment generation, formula replication, orchestration and oracle work.
- UNSAT is established here by exhaustive enumeration, not inferred from a rejected witness.
- Input size includes clause count and literals; brute-force observations are not SAT lower bounds.
- first_attack.json is preserved arithmetic-only bookkeeping, not an executed verifier.
