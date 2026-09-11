# Google Borg BigQuery v8 results

status: paired scheduler stratification observation
window: first 24 hours

| cell | strata | started | closed | right-censored |
|---|---:|---:|---:|---:|
| a | 95 | 7820880 | 6646807 | 1174073 |
| b | 92 | 9301457 | 8561541 | 739916 |

Conservation audit: PASS independently for both cells.

The dominant scheduler strata differ across cells. Cell a is led by priority 200/class 1, while cell b is led by priority 0/class 0. Several shared priority/class combinations have different interruption and duration profiles. This supports treating scheduler composition as a boundary condition, not as noise to pool away.

No causal priority claim is made.
