# Parameterized contract-state scaling v1: results

The family `G_n` uses an n-bit unresolved-obligation mask. Every mask is reachable, and `inspect` accepts exactly the zero mask.

## Scaling result

| n | K_G | I_G bits | Pairwise distinguishable | Maximum distinguishing depth | Update work | Decision work |
|---:|---:|---:|---|---:|---:|---:|
| 1 | 2 | 1 | yes | 1 | 1 | 1 |
| 2 | 4 | 2 | yes | 2 | 1 | 2 |
| 3 | 8 | 3 | yes | 3 | 1 | 3 |
| 4 | 16 | 4 | yes | 4 | 1 | 4 |
| 5 | 32 | 5 | yes | 5 | 1 | 5 |
| 6 | 64 | 6 | yes | 6 | 1 | 6 |
| 7 | 128 | 7 | yes | 7 | 1 | 7 |
| 8 | 256 | 8 | yes | 8 | 1 | 8 |

The measured family follows:

\[
K_{G_n}=2^n,
\qquad
I_{G_n}=n.
\]

The modeled lifecycle dimensions separate:

\[
T_U(n)=O(1)
\]

for an event that touches one bit, from:

\[
T_V(n)=O(n)
\]

for an inspection that scans the obligation mask. Evidence state size is n bits.

Maximum distinguishing depth is n in this family: two nonzero masks can require satisfying all bits of the smaller mask before inspection separates them. This is a deliberately simple family, but it demonstrates that state-information complexity, update complexity, decision complexity, and distinguishing depth are distinct axes.

The exponential state count is not itself an exponential bit requirement: identifying one of `2^n` states takes n ideal bits. Conversely, compact state does not imply cheap update or decision in a general family; those costs depend on the transition and observation mechanisms.

All values are exact for the frozen finite family and modeled unit costs, not empirical wall-clock benchmarks. No P/NP conclusion follows.
