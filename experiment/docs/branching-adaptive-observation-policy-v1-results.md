# Branching adaptive observation-policy calibration v1: results

This synthetic fixture has five hidden states and an exact-identification contract. The policy is genuinely branching:

```text
cheap_local
├── easy_A → stop
├── easy_B → stop
└── uncertain → second_local
    ├── local_C → stop
    ├── local_D → stop
    └── local_uncertain → privileged_exact
```

Per-state modeled observation costs:

| State | Cost |
|---|---:|
| A | 1 |
| B | 1 |
| C | 3 |
| D | 3 |
| E | 9 |

The policy identifies all five states exactly. Its worst-case cost is:

\[
C_{\mathrm{worst}}=9.
\]

With the declared uniform prior:

\[
\mathbb E[C_O]=\frac{1+1+3+3+9}{5}=3.4.
\]

Always invoking privileged exact telemetry costs 6, so the adaptive policy is cheaper in expectation but more expensive in the worst case:

\[
3.4<6<9.
\]

This is a finite synthetic result. It demonstrates why expected and worst-case observation cost must be reported separately. It does not establish an optimal policy for arbitrary observation trees, actual hardware energy, or a P/NP result.

The policy illustrates attention as conditional escalation: stop as soon as the contract is resolved, acquire a second local distinction when needed, and invoke privileged observation only for the residual ambiguity.
