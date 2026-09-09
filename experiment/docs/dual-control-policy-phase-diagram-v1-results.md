# Dual-control policy phase diagram v1: results

For the synthetic fragile/sturdy contract, compare:

\[
C_{\mathrm{immediate}}=1+100\min(p,1-p),
\]
\[
C_{\mathrm{touch}}=2+10p,
\]
\[
C_{\mathrm{inspect}}=6.
\]

The lower envelope changes policy as the fragile-state prior changes. Analytic thresholds are:

- immediate/touch: \(p=1/90\approx0.0111\);
- touch/inspect: \(p=0.4\);
- inspect/immediate: \(p=0.95\).

A grid sweep at resolution \(0.001\) produced:

| Policy | Grid interval |
|---|---|
| Immediate action | \([0,0.011]\) |
| Gentle informative intervention | \([0.012,0.399]\) |
| Non-destructive inspection | \([0.4,0.95]\) |
| Immediate action | \([0.951,1]\) |

Thus the optimal policy is non-monotonic in the prior:

\[
\boxed{
\text{act}\rightarrow\text{experiment}\rightarrow\text{inspect}\rightarrow\text{act}
}
\]

The result is a synthetic modeled-cost phase diagram. It does not establish a universal policy law or physical object-risk measurement.
