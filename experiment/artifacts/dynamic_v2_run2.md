# Dynamic dependency consequence v2: executed results

Cells: 288; policies: selective_repair, certificate_repair, delayed_certificate, unchecked_cache.
Costs below use the declared default stale-failure rate and downstream penalty.
Counters and consequence penalties are synthetic logical units, not runtime, energy, money, or incident probabilities.

## Aggregate total modeled cost

| Policy | Total modeled cost | Wrong outputs | Unsafe reuse | Stale failures |
|---|---:|---:|---:|---:|
| selective_repair | 629624 | 766 | 766 | 1408 |
| certificate_repair | 534520 | 0 | 0 | 0 |
| delayed_certificate | 566749 | 293 | 293 | 401 |
| unchecked_cache | 533664 | 2088 | 2088 | 4878 |

## Break-even surface winner counts

| Penalty | Policy wins/ties |
|---:|---|
| 0 | {'selective_repair': 48, 'unchecked_cache': 288} |
| 10 | {'selective_repair': 48, 'unchecked_cache': 288} |
| 100 | {'selective_repair': 106, 'certificate_repair': 44, 'delayed_certificate': 23, 'unchecked_cache': 168} |
| 1000 | {'selective_repair': 192, 'certificate_repair': 96, 'delayed_certificate': 50, 'unchecked_cache': 24} |
| 10000 | {'selective_repair': 192, 'certificate_repair': 96, 'delayed_certificate': 50, 'unchecked_cache': 24} |

A surface winner is a least-modeled-cost policy for that cell and penalty. Ties are credited to every tied policy.

Certificate validation is a modeled input channel, not proof of semantic truth. Hidden drift, failure rates, and downstream penalties are synthetic. No P/NP or deployment claim follows.
