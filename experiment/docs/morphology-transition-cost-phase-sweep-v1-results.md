# Morphology transition-cost phase sweep v1: results

A deterministic continuous demand path of 500 periods was swept over entry and exit costs \(S_{R\to L},S_{L\to R}\in\{0,2,6,10,20\}\). The instantaneous operating crossover is \(d=1\). Lock-in is time spent in local morphology below \(d=1\), or remote morphology above \(d=1\).

The threshold policy was compared with an exact finite-horizon Bellman oracle on the same realized path and cost cell. The oracle knows the declared realized demand path; this is a bounded continuation benchmark, not a claim about online learning.

Representative cells:

| \(S_{R\to L}\) | \(S_{L\to R}\) | Heuristic | Optimal | Heuristic regret | Heuristic lock-in | Optimal lock-in |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 1107.36 | 1107.36 | 0.00 | 0.000 | 0.000 |
| 2 | 2 | 1168.94 | 1161.44 | 7.51 | 0.062 | 0.002 |
| 6 | 6 | 1343.78 | 1269.44 | 74.35 | 0.192 | 0.002 |
| 10 | 10 | 1658.75 | 1377.44 | 281.31 | 0.392 | 0.002 |
| 20 | 20 | 1553.11 | 1537.57 | 15.54 | 0.516 | 0.482 |

At \((20,20)\), the optimal continuation also retains remote morphology through a substantial locally unfavorable region. This is evidence of rational lock-in within the declared finite-horizon fixture: the optimal policy has nonzero lock-in exposure, while the heuristic has only 15.54 additional cost.

At \((10,10)\), the threshold policy has substantial observed persistence but 281.31 regret relative to the exact continuation oracle. This is maladaptive persistence under the benchmark, not merely behavioral lock-in.

The sweep therefore separates four properties rather than conflating them:

- behavioral persistence: morphology remains despite instantaneous operating preference;
- rational persistence: the exact continuation oracle also retains it;
- amortization: persistence reduces total cost relative to a more reactive alternative;
- maladaptive lock-in: persistence has positive regret against a feasible lower-cost continuation policy.

The bounded result is:

\[
\boxed{\text{Persistence is a behavior; efficiency is a path property; optimality requires a continuation benchmark.}}
\]

All demand dynamics and costs are synthetic modeled quantities.
