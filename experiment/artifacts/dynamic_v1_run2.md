# Dynamic dependency repair v1: executed results

Listed logical operation counters, not runtime, energy, money, or hardware measurements.
Cells: 144; policies: cold_recompute, selective_repair, full_reset, certificate_repair, unchecked_cache.

## Aggregate policy totals

| Policy | Operations | Wrong outputs | Stale acceptances |
|---|---:|---:|---:|
| cold_recompute | 104832 | 0 | 0 |
| selective_repair | 258602 | 47 | 12 |
| full_reset | 194688 | 47 | 0 |
| certificate_repair | 262940 | 0 | 0 |
| unchecked_cache | 22932 | 1044 | 1044 |

## Strict exactness winners

{'selective_repair': 12, 'full_reset': 12, 'unchecked_cache': 12, 'cold_recompute': 132}

A strict winner is the least-operation policy among policies that were exact on that cell. Cells are paired by generated seed and are not independent population samples.

## Interpretation boundary

The certificate policy is a modeled validation channel, not cryptographic proof of semantic truth. Hidden drift is synthetic. These finite runs test dependency repair and stale-state accounting; they establish no dynamic lower bound, deployment result, or P/NP claim.
