# Semantic interaction calibration v1

| Case | Join | Union | Joint | Interaction | Union exact | Aware exact |
|---|---:|---:|---:|---:|---|---|
| disjoint | 1 | 2 | 2 | 0 | True | True |
| disjoint | 2 | 4 | 4 | 0 | True | True |
| disjoint | 4 | 8 | 8 | 0 | True | True |
| adjacent | 1 | 2 | 2 | 0 | True | True |
| adjacent | 2 | 3 | 3 | 0 | True | True |
| adjacent | 4 | 5 | 5 | 0 | True | True |
| joint | 1 | 2 | 3 | 1 | False | True |
| joint | 2 | 3 | 4 | 1 | False | True |
| joint | 4 | 5 | 6 | 1 | False | True |
| cluster | 1 | 4 | 5 | 1 | False | True |
| cluster | 2 | 5 | 6 | 1 | False | True |
| cluster | 4 | 7 | 8 | 1 | False | True |

Joint constraints are explicit fixture rules, not inferred semantic evidence. Timing is diagnostic local data.
