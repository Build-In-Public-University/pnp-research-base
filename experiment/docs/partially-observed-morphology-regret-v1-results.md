# Partially observed morphology regret v1: results

The hidden regime is low or high with prior 1/2. Observed demands overlap across regimes, so the future is not identified by the current observation. A 12-step exact online Bayes dynamic program was compared with an instantaneous threshold heuristic and a clairvoyant realized-path oracle.

| Policy | Cost |
|---|---:|
| Heuristic | 72.000 |
| Bayes online | 45.000 |
| Clairvoyant | 43.000 |

The telescoping decomposition is exact:

\[
R_{\mathrm{struct}}
=72-43
=29
=\underbrace{72-45}_{R_{\mathrm{policy}}=27}
+\underbrace{45-43}_{R_{\mathrm{uncertainty}}=2}.
\]

The heuristic loses 27 modeled cost units because its decision rule is inferior. The Bayes agent loses 2 because it does not know the future observations and regime. The clairvoyant oracle is a hindsight benchmark, not an online policy.

This is a single seeded path and a synthetic emission model. It demonstrates an auditable decomposition, not a general estimate of forecast or information value.
