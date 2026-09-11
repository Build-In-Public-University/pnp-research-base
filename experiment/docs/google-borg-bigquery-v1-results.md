# Google Borg BigQuery v1 results

status: remote_aggregate_observation
table: `google.com:google-cluster-data.clusterdata_2019_a.collection_events`
job_id: bqjob_r3d6da8ae3edfaa56_000001a0908cf859_1
bytes_processed: 332919056
bytes_billed: 333447168
aggregate_rows: 100
missing_bucket_indices: [1]

| event | count |
|---|---:|
| submit_count | 85403 |
| queue_count | 2675 |
| enable_count | 86542 |
| schedule_count | 85685 |
| evict_count | 0 |
| fail_count | 435 |
| finish_count | 12567 |
| kill_count | 57371 |
| lost_count | 0 |

| diagnostic | value |
|---|---:|
| peak submit bucket/count | 0 / 16515 |
| peak queue-event bucket/count | 0 / 1614 |
| peak finish bucket/count | 20 / 389 |

Boundary: observational remote aggregate; no controlled capacity claim.
