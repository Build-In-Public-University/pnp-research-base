# Capability-space routing calibration v1

A two-node system must satisfy a contract requiring the composite capability `{parity, group}`. Node `i` has `parity`; node `j` has `group`. The agent starts at `i` with only `parity` reachable and no knowledge of `j`'s capability.

Actions are `discover` (cost 1), `move` to `j` (cost 5), `connect` a trusted remote link (cost 2), `transfer` the discovered capability (cost 2), and `compose` the two local capabilities (cost 1). The experiment computes least-cost valid routes and records the evolving reachable capability set.
