# Google Borg BigQuery v5 protocol

This protocol joins the v4 pressure buckets to remote five-minute aggregates of Google Borg task usage and machine capacity. `instance_usage.average_usage.cpus` and `.memory` are summed by bucket. Capacity is the sum of each machine's maximum recorded CPU and memory capacity from `machine_events`.

The resulting CPU and memory values are normalized task-usage proxies, not direct physical utilization: task usage can exceed physical capacity under overcommit and capacity is held as a static reference. Bucket 0 is excluded from correlation because it is the trace-start boundary.

Only aggregate rows, hashes, job IDs, and query cost metadata are emitted.
