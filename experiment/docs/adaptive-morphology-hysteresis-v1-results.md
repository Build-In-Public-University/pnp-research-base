# Adaptive morphology hysteresis calibration v1: results

Remote service costs `3d` per period. Local service plus maintenance costs `d+2` per period. Switching costs are:

\[
C_{R\to L}=10,
\qquad
C_{L\to R}=6.
\]

An exact four-step dynamic program gives different switching thresholds depending on current morphology:

- starting remote, local becomes worthwhile at \(d>2.25\) (tie at 2.25; the implementation's deterministic tie-break selects local);
- starting local, remote becomes worthwhile at \(d<0.25\) (tie at 0.25; the implementation retains local).

The resulting hysteresis band is approximately:

\[
0.25\le d\le2.25.
\]

Within this band, the optimal action is to retain the current morphology rather than switch at the instantaneous running-cost crossover \(d=1\).

| Demand | Start remote | Start local |
|---:|---|---|
| 0.1 | remote | remote |
| 0.25 | remote | local |
| 1 | remote | local |
| 2 | remote | local |
| 2.25 | local | local |
| 3 | local | local |

This is a finite synthetic dynamic-programming result. It establishes switching-cost-induced hysteresis in the fixture; it is not a biological law or a measured deployment policy.
