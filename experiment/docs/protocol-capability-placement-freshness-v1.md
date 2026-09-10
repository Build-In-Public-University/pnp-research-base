# Capability placement freshness calibration v1

Extend persistent capability reuse with change rate lambda. Fresh discovery remains 11 per request. Persistent remote routing pays setup 8 and invocation 3. A local replica pays setup 15, local invocation 1, and expected refresh/validation cost 12 lambda per invocation. Evaluate demand n=1..12 and lambda in {0, .05, .1, .2, .4}.

The local replica is modeled as contract-valid after each expected refresh/validation charge; no stale result is silently accepted. Costs are synthetic expected units, not physical measurements.
