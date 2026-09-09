# Interactive observation-policy calibration v1: results

This bounded synthetic experiment contains two hidden machine states:

```text
low_power:  ordinary observation = (same_time, same_cpu, same_bytes), energy = 1.0
high_power: ordinary observation = (same_time, same_cpu, same_bytes), energy = 2.0
```

The energy labels are synthetic. This is not a measurement of the M3 Max.

## Policy comparison

| Policy | Energy identifiable | Observation cost | Measurement perturbation |
|---|---|---:|---|
| Passive ordinary observation | no | 1 | no |
| Privileged telemetry | yes | 4 | yes |
| Active calibration | yes | 11 | yes |

The passive policies generate identical action/observation transcripts for the two hidden states:

\[
\tau_{\mathrm{passive}}(S_1)=\tau_{\mathrm{passive}}(S_2)
\]

while:

\[
E(S_1)\ne E(S_2).
\]

Therefore no exact estimator from the passive transcript can recover the hidden energy value for both states.

Privileged telemetry adds a direct energy observation. Active calibration obtains a low/high energy classification by interacting with the system, at a higher modeled observation cost. Both are different observation architectures, not merely different post-processing algorithms.

The result supports:

\[
\boxed{
\text{Identifiability depends on the observation policy and its authorized actions.}
}
\]

The measurement action itself can perturb scheduling, cache state, thermal state, and energy. The perturbation flag is therefore retained rather than treating observation as free.

This is a structural synthetic result. It does not establish actual energy values, package energy, wall energy, or a P/NP result.
