# Adaptive observation-policy calibration v1

Four hidden states must be identified exactly. Three authorized observation channels return different partitions: `local_parity` costs 1 and returns state parity; `local_group` costs 3 and returns state group; `privileged_exact` costs 6 and returns the exact state. Passive observation returns the same `nominal` value for all states.

The adaptive policy chooses the next channel from observations already received. Exhaustive finite policy search compares fixed channel sequences and selects the least-cost sufficient policy. All values are synthetic modeled units; this is a policy/identifiability experiment, not hardware telemetry.
