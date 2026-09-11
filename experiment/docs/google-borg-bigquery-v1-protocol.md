# Google Borg BigQuery v1 protocol

This protocol queries Google’s public `clusterdata_2019_a.collection_events` table through BigQuery. Raw trace rows are not downloaded or stored locally. The query projects only five-minute event counts by lifecycle event type.

Event mapping follows Google’s published trace schema: `0=SUBMIT`, `1=QUEUE`, `2=ENABLE`, `3=SCHEDULE`, `4=EVICT`, `5=FAIL`, `6=FINISH`, `7=KILL`, `8=LOST`.

The query is frozen in `sources/google-borg/collection_event_buckets.sql`. The receipt records the SQL hash, public table, BigQuery project, job ID, bytes processed/billed, aggregate output hash, and missing bucket indices.

Privacy boundary: no `user`, collection names, IDs, or raw event records are projected into the aggregate.

This is an observational remote aggregate. It is not a controlled capacity experiment.
