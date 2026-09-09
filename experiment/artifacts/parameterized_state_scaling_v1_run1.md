# Parameterized contract-state scaling v1

| n | K_G | I_G bits | Pairwise | Max depth | Update | Decision |
|---:|---:|---:|---|---:|---:|---:|
| 1 | 2 | 1 | True | 1 | 1 | 1 |
| 2 | 4 | 2 | True | 2 | 1 | 2 |
| 3 | 8 | 3 | True | 3 | 1 | 3 |
| 4 | 16 | 4 | True | 4 | 1 | 4 |
| 5 | 32 | 5 | True | 5 | 1 | 5 |
| 6 | 64 | 6 | True | 6 | 1 | 6 |
| 7 | 128 | 7 | True | 7 | 1 | 7 |
| 8 | 256 | 8 | True | 8 | 1 | 8 |

The family receipt separates exponential semantic-state count from linear information bits, constant modeled bit-update work, and linear decision scan work.
