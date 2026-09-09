# Loss-aware adaptive observation v1: results

This synthetic calibration changes the contract from exact hidden-state identification to a binary decision: `safe` or `escalate`. State `E` is escalation-worthy; states `A` through `D` are safe. Wrong decisions incur finite loss 20. Privileged observation costs 6.

After a cheap observation and a local refinement, the residual class contains safe state `D` and risky state `E`. The policy compares stopping risk with privileged-observation cost.

| Scenario | Residual risky probability | Stop risk | Policy | Expected total cost |
|---|---:|---:|---|---:|
| Common/high-loss | 0.5 | 10 | Observe privileged | 4.6 |
| Rare/low-loss | 0.1 | 2 | Stop safely | 1.06 |

The common case escalates because:

\[
R(\tau)=0.5\times20=10>6.
\]

The rare case stops with residual uncertainty because:

\[
R(\tau)=0.1\times20=2<6.
\]

The rare policy is not exact-state identifying. That is intentional: under a finite-loss contract, exact knowledge is not always worth purchasing.

The result supports the stopping recursion:

\[
V(\tau)=\min\left[R(\tau),\min_a\left(C_O(a)+\mathbb E_o[V(\tau,a,o)]\right)\right].
\]

It also separates expected policy cost from information completeness. A policy can be rationally cheaper while leaving some physical uncertainty unresolved.

All states, probabilities, losses, and costs are synthetic modeled values. This is not hardware telemetry, a general optimal-policy solver, or a P/NP result.
