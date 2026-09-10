# Stochastic morphology switching v1: results

A deterministic seeded Markov demand path of 500 periods was used, with demand values \(d\in\{0.1,1.0,4.0\}\). Remote operating cost is \(3d\); local operating plus maintenance cost is \(d+2\).

| Agent | Total | Operating | Transition | Switches | Regret vs best fixed | Remote / Local |
|---|---:|---:|---:|---:|---:|---:|
| Stateless | 1615.4 | 1499.4 | 116.0 | 58 | -222.4 | 331 / 169 |
| Symmetric | 1609.4 | 1499.4 | 110.0 | 55 | -228.4 | 266 / 234 |
| Adaptive | 1941.4 | 1499.4 | 442.0 | 55 | 103.6 | 266 / 234 |

The three policies have identical operating cost on this realized path. The adaptive and symmetric policies also have identical switch counts and occupancy. Their entire total-cost difference is transition accounting:

\[
442-110=332,
\qquad
1941.4-1609.4=332.0.
\]

The adaptive policy reduced switching relative to stateless routing, but did not minimize cumulative cost because its larger transition prices dominated. The symmetric policy was cheapest in this fixture.

This negative result matters: hysteresis can reduce structural churn without automatically creating economic value. Structural persistence can produce amortization or lock-in depending on the transition prices and workload.

Regret is relative to the cheaper always-remote or always-local policy on this same realized path. All costs and demand dynamics are synthetic modeled quantities.
