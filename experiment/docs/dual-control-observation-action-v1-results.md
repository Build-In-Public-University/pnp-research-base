# Dual-control observation/action calibration v1: results

A hidden object is `fragile` or `sturdy`. The terminal contract is to choose the correct handling action. Immediate handling costs 1 and incurs wrong-action loss 100. Non-destructive inspection costs 5 and reveals the state. Gentle touch costs 1, reveals the state, and damages a fragile object with modeled cost 10. Correct handling costs 1.

The expected policy costs are:

\[
C_{\mathrm{immediate}}=1+100\min(p,1-p),
\]

\[
C_{\mathrm{inspect}}=5+1=6,
\]

\[
C_{\mathrm{touch}}=1+1+10p.
\]

| Scenario | Immediate | Inspect | Gentle touch | Preferred policy |
|---|---:|---:|---:|---|
| Rare fragile, \(p=0.1\) | 11 | 6 | 3 | Gentle touch |
| Common fragile, \(p=0.5\) | 51 | 6 | 7 | Inspect |

Gentle touch is a dual-control action: it changes the object and reveals its state. In the rare-fragile scenario, its modeled damage risk is worth accepting because it buys information cheaply. In the common-fragile scenario, non-destructive inspection is preferred.

The result supports:

\[
\boxed{
\text{Embodied intelligence chooses actions partly for what they change and partly for what they reveal.}
}
\]

This is a finite synthetic cost comparison, not a physical experiment, actual object-risk estimate, or P/NP result.
