# Capability placement freshness calibration v1: results

The local replica has setup cost 15, local invocation cost 1, and expected refresh/validation cost `12 lambda` per invocation:

\[
C_{\mathrm{local}}(n,\lambda)=15+n+12\lambda n.
\]

The persistent remote route remains fresh through its source of truth:

\[
C_{\mathrm{remote}}(n)=8+3n.
\]

Fresh discovery remains:

\[
C_{\mathrm{fresh}}(n)=11n.
\]

The 60-cell sweep gives:

| Change rate \(\lambda\) | \(n=1\) | \(n=4\) | \(n=12\) |
|---:|---|---|---|
| 0 | Fresh | Local | Local |
| 0.05 | Fresh | Remote | Local |
| 0.1 | Fresh | Remote | Local |
| 0.2 | Fresh | Remote | Remote |
| 0.4 | Fresh | Remote | Remote |

At zero change rate, demand eventually favors locality. As \(\lambda\) increases, refresh and validation erode the local marginal advantage. In this model the remote/local crossover satisfies:

\[
15+n+12\lambda n=8+3n,
\]

so locality wins only when:

\[
n(2-12\lambda)>7.
\]

For \(\lambda\ge1/6\), the local replica has no marginal-cost advantage at all. This is a bounded synthetic expected-cost result; it is not a measurement of real change processes, staleness probabilities, or network performance.
