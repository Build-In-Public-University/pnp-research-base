# Action-relative value-of-information v1: results

The fragile/sturdy fixture is evaluated at beliefs \(p=0.1\) and \(p=0.9\). Their binary Shannon entropies are equal:

\[
H(0.1)=H(0.9)=0.468995593589\text{ bits}.
\]

The perfect-information reduction in immediate wrong-decision risk is also equal at both beliefs:

\[
VOI_{\mathrm{perfect}}=10.
\]

But the action-conditioned costs differ:

| Belief | Entropy | Perfect-info VOI | Touch | Inspect | Best |
|---|---:|---:|---:|---:|---|
| \(p=0.1\) | 0.468995593589 | 10 | 3 | 6 | Touch |
| \(p=0.9\) | 0.468995593589 | 10 | 11 | 6 | Inspect |

The policy changes because touching is costly when the object is fragile:

\[
C_{\mathrm{touch}}=2+10p.
\]

Thus entropy alone cannot determine the rational attention policy. The relevant object includes belief, available actions, state-conditioned consequences, observation value, physical cost, and the contract:

\[
\boxed{
\pi^*=f(\text{belief},\text{actions},\text{consequences},\text{observation value},\text{cost},G).
}
\]

This is a synthetic modeled-cost counterexample, not a physical risk measurement or a universal policy law.
