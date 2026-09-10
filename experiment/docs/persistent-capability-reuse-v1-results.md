# Persistent capability reuse calibration v1: results

Three strategies serve repeated requests for a contract requiring local `parity` and remote `group`:

| Strategy | Setup | Per invocation |
|---|---:|---:|
| Fresh discovery/reconnection | 0 | 11 |
| Persistent remote route | 8 | 3 |
| Local replica | 15 | 1 |

Therefore:

\[
C_{\mathrm{fresh}}(n)=11n,
\]
\[
C_{\mathrm{remote}}(n)=8+3n,
\]
\[
C_{\mathrm{local}}(n)=15+n.
\]

The least-cost strategy changes with demand:

| Demand | Best strategy |
|---:|---|
| \(n=1\) | Fresh (tie with persistent remote) |
| \(n=2,3\) | Persistent remote |
| \(n\ge4\) | Local replica |

The remote/local crossover occurs when:

\[
8+3n>15+n,
\]

or:

\[
n>3.5.
\]

This supports a bounded amortization result: one-time discovery and connection reduce marginal invocation cost, while sufficiently high repeated demand justifies moving the capability closer to the workload. Costs are synthetic modeled units, not physical network measurements.
