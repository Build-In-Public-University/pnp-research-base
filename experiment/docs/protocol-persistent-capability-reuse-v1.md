# Persistent capability reuse calibration v1

Compare three strategies for repeated requests requiring remote `group` plus local `parity`: fresh discovery/reconnection on every request; one-time discovery, movement, and trusted connection with repeated remote invocation; and one-time local replication followed by local execution.

Synthetic costs per request sequence:

- fresh: 11 per request;
- persistent remote: setup 8, invocation 3;
- local replica: setup 15, invocation 1.

Evaluate n = 1..12 requests, total cost, average cost, and the least-cost strategy. These are modeled costs, not physical measurements.
