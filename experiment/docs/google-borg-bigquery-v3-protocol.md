# Google Borg BigQuery v3 protocol

This protocol reconstructs attempt-level lifecycle records remotely from the first 24 hours of Google’s public `clusterdata_2019_a.instance_events` table. An attempt starts at each `SCHEDULE` event and closes at the first subsequent `EVICT`, `FAIL`, `FINISH`, `KILL`, or `LOST` event for the same `(collection_id, instance_index)` identity.

The query emits only aggregate counts and approximate duration quantiles. It never downloads raw task events. The 24-hour window is frozen as `0 <= time < 86,400,000,000` microseconds. Attempts without a terminal event inside the window are right-censored rather than treated as completed.

The previous full-table lifecycle envelope query remains separate; this protocol is not a mutation of that receipt.
