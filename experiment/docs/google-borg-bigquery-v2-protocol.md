# Google Borg BigQuery v2 protocol

This protocol remotely aggregates Google’s public `clusterdata_2019_a.instance_events` table. It projects only event type, timestamp, collection ID, and instance index inside BigQuery, then emits one aggregate row. Raw task rows are never downloaded.

The grouping key is `(collection_id, instance_index)`. For each key, the query records the first `SUBMIT`, first `SCHEDULE`, and latest terminal/interruption event (`EVICT`, `FAIL`, `FINISH`, `KILL`, `LOST`). This deliberately produces a lifecycle envelope. It is not a per-attempt reconstruction because retries and evictions can reuse the same identity.

The query emits counts and approximate quantiles for submit-to-schedule wait and schedule-to-terminal envelope duration. The latter must not be described as clean service time without an attempt-level reconstruction.
