# Fixed-contract architecture v1

| n | Architecture | Exact | Retained bits | Update | Decision | Evidence |
|---:|---|---|---:|---:|---:|---:|
| 1 | raw_mask | True | 1 | 2 | 1 | 0 |
| 1 | mask_counter | True | 2 | 2 | 1 | 1 |
| 1 | sparse_set | True | 1 | 2 | 1 | 1 |
| 1 | event_log | True | 6 | 2 | 3 | 2 |
| 2 | raw_mask | True | 2 | 4 | 2 | 0 |
| 2 | mask_counter | True | 4 | 4 | 1 | 1 |
| 2 | sparse_set | True | 2 | 4 | 1 | 1 |
| 2 | event_log | True | 15 | 4 | 5 | 2 |
| 3 | raw_mask | True | 3 | 6 | 3 | 0 |
| 3 | mask_counter | True | 5 | 6 | 1 | 1 |
| 3 | sparse_set | True | 6 | 6 | 1 | 1 |
| 3 | event_log | True | 21 | 6 | 7 | 2 |
| 4 | raw_mask | True | 4 | 8 | 4 | 0 |
| 4 | mask_counter | True | 7 | 8 | 1 | 1 |
| 4 | sparse_set | True | 8 | 8 | 1 | 1 |
| 4 | event_log | True | 36 | 8 | 9 | 2 |
| 5 | raw_mask | True | 5 | 10 | 5 | 0 |
| 5 | mask_counter | True | 8 | 10 | 1 | 1 |
| 5 | sparse_set | True | 15 | 10 | 1 | 1 |
| 5 | event_log | True | 44 | 10 | 11 | 2 |
| 6 | raw_mask | True | 6 | 12 | 6 | 0 |
| 6 | mask_counter | True | 9 | 12 | 1 | 1 |
| 6 | sparse_set | True | 18 | 12 | 1 | 1 |
| 6 | event_log | True | 52 | 12 | 13 | 2 |
| 7 | raw_mask | True | 7 | 14 | 7 | 0 |
| 7 | mask_counter | True | 10 | 14 | 1 | 1 |
| 7 | sparse_set | True | 21 | 14 | 1 | 1 |
| 7 | event_log | True | 60 | 14 | 15 | 2 |
| 8 | raw_mask | True | 8 | 16 | 8 | 0 |
| 8 | mask_counter | True | 12 | 16 | 1 | 1 |
| 8 | sparse_set | True | 24 | 16 | 1 | 1 |
| 8 | event_log | True | 85 | 16 | 17 | 2 |

All architectures implement the same fixed contract; costs are modeled units, not timings.
