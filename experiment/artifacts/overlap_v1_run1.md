# Overlapping updates calibration v1

| Pattern | Join width | Isolated sum | Union | Overlap savings | Exact |
|---|---:|---:|---:|---:|---|
| single | 1 | 1 | 1 | 0 | True |
| single | 1 | 1 | 1 | 0 | True |
| single | 2 | 2 | 2 | 0 | True |
| single | 2 | 2 | 2 | 0 | True |
| single | 4 | 4 | 4 | 0 | True |
| single | 4 | 4 | 4 | 0 | True |
| disjoint | 1 | 2 | 2 | 0 | True |
| disjoint | 1 | 2 | 2 | 0 | True |
| disjoint | 2 | 4 | 4 | 0 | True |
| disjoint | 2 | 4 | 4 | 0 | True |
| disjoint | 4 | 8 | 8 | 0 | True |
| disjoint | 4 | 8 | 8 | 0 | True |
| adjacent | 1 | 2 | 2 | 0 | True |
| adjacent | 1 | 2 | 2 | 0 | True |
| adjacent | 2 | 4 | 3 | 1 | True |
| adjacent | 2 | 4 | 3 | 1 | True |
| adjacent | 4 | 8 | 5 | 3 | True |
| adjacent | 4 | 8 | 5 | 3 | True |
| cluster | 1 | 4 | 4 | 0 | True |
| cluster | 1 | 4 | 4 | 0 | True |
| cluster | 2 | 8 | 5 | 3 | True |
| cluster | 2 | 8 | 5 | 3 | True |
| cluster | 4 | 16 | 7 | 9 | True |
| cluster | 4 | 16 | 7 | 9 | True |

Counts are local instrument outputs over temporary copies; timing is diagnostic, not universal evidence.
