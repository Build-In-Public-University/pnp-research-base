# History experiment v1.1: corrected executed results

Costs: listed unit-weight operation counters, NOT time or physical energy.
World/input generation, feed production and oracle/serialization work excluded.

## Representative seed 1, n=64 (initial setup + 32 updates)

| Changed inputs per step | Feed | Cold ops/errors | Snapshot ops/errors | Unchecked ops/errors | Feed repair ops/errors |
|---|---|---|---|---|---|
| 0 | complete | 40161/0 | 8065/0 | 1249/0 | 1921/0 |
| 0 | omitted | 40161/0 | 8065/0 | 1249/0 | 1921/0 |
| 1 | complete | 40161/0 | 11425/0 | 1249/32 | 5377/0 |
| 1 | omitted | 40161/0 | 11425/0 | 1249/32 | 3541/32 |
| 16 | complete | 40161/0 | 46633/0 | 1249/32 | 42025/0 |
| 16 | omitted | 40161/0 | 46633/0 | 1249/32 | 28273/32 |
| 64 | complete | 40161/0 | 75649/0 | 1249/24 | 75649/0 |
| 64 | omitted | 40161/0 | 75649/0 | 1249/24 | 63361/24 |

Errors mean wrong returned vector/total/decision; not necessarily false acceptance.

## Paired exact-policy outcomes (complete-feed cells only to avoid duplicate worlds)

- n=16, changes=0: {'snapshot_wins': 3} across three seeds.
- n=16, changes=1: {'snapshot_wins': 3} across three seeds.
- n=16, changes=4: {'cold_wins': 3} across three seeds.
- n=16, changes=16: {'cold_wins': 3} across three seeds.
- n=64, changes=0: {'snapshot_wins': 3} across three seeds.
- n=64, changes=1: {'snapshot_wins': 3} across three seeds.
- n=64, changes=16: {'cold_wins': 3} across three seeds.
- n=64, changes=64: {'cold_wins': 3} across three seeds.

## Safety totals (cell-step observations, NOT independent population samples)

- complete, cold: wrong outputs=0, false accepts=0, false rejects=0.
- complete, incremental_snapshot: wrong outputs=0, false accepts=0, false rejects=0.
- complete, unchecked: wrong outputs=528, false accepts=337, false rejects=0.
- complete, incremental_feed: wrong outputs=0, false accepts=0, false rejects=0.
- omitted, cold: wrong outputs=0, false accepts=0, false rejects=0.
- omitted, incremental_snapshot: wrong outputs=0, false accepts=0, false rejects=0.
- omitted, unchecked: wrong outputs=528, false accepts=337, false rejects=0.
- omitted, incremental_feed: wrong outputs=522, false accepts=49, false rejects=0.

## Priced consequence winners (all cells; ties credited to every winner)

Synthetic price per wrong output; no implied permission to violate correctness.
- penalty=0: {'unchecked': 48}
- penalty=10: {'unchecked': 48}
- penalty=100: {'unchecked': 48}
- penalty=1000: {'unchecked': 24, 'incremental_feed': 6, 'incremental_snapshot': 6, 'cold': 12}
- penalty=10000: {'unchecked': 12, 'incremental_feed': 6, 'incremental_snapshot': 6, 'cold': 24}

## Strict observed-correctness winners (all cells)

{'unchecked': 12, 'incremental_feed': 6, 'incremental_snapshot': 6, 'cold': 24}

Each cell stores an exact rational break-even price against its cheapest observed-exact policy.
Observed-exact eligibility is retrospective for this trajectory, not a guarantee for future inputs.
Cells sharing a trajectory or differing only in feed visibility are paired, not independent evidence.
No universal winner, dynamic solver optimality, physical cost, AI effect, or P/NP inference follows.
