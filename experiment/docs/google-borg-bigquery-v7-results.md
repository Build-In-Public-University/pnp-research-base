# Google Borg BigQuery v7 results

status: remote scheduler stratification observation
cell: b
window: first 24 hours
job_id: bqjob_r452ae371036fa639_000001a091092c51_1
bytes_processed: 102739916768
bytes_billed: 102740525056
strata_rows: 92

Conservation audit: PASS for started, closed, right-censored, evicted, failed, finished, killed, and lost counts.

Top strata by started attempts:

| priority | scheduling class | collection type | CPU bin | memory bin | started | closed | censored | evicted | p50 s | p90 s |
|---:|---:|---:|---|---|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | <=0.1 | <=1 | 3610163 | 3538617 | 71546 | 2225200 | 225.702621 | 1394.030405 |
| 103 | 1 | 0 | <=0.1 | <=1 | 894465 | 826300 | 68165 | 38774 | 839.53473 | 13596.251026 |
| 360 | 2 | 0 | <=0.1 | <=1 | 829364 | 818413 | 10951 | 194924 | 358.419139 | 2887.963948 |
| 101 | 2 | 1 | <=0.1 | <=1 | 792425 | 783373 | 9052 | 0 | 366.341257 | 3192.871402 |
| 103 | 0 | 0 | <=0.1 | <=1 | 612616 | 516955 | 95661 | 40195 | 2619.423833 | 30085.819918 |
| 0 | 2 | 0 | <=0.1 | <=1 | 433311 | 430802 | 2509 | 207965 | 465.609529 | 3172.123251 |
| 105 | 0 | 0 | <=0.1 | <=1 | 371059 | 361291 | 9768 | 187 | 84.353722 | 2827.16578 |
| 25 | 2 | 0 | <=0.1 | <=1 | 357247 | 352056 | 5191 | 348737 | 252.821694 | 1810.81637 |

Interpretation: scheduler descriptors partition markedly different interruption and duration profiles. This is evidence for heterogeneity and a reason not to treat pooled cell-level associations as a single mechanism. It is not causal evidence because priority and class were not randomized.
