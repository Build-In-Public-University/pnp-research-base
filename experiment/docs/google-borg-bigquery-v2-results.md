# Google Borg BigQuery v2 results

status: remote_lifecycle_envelope_observation
table: `google.com:google-cluster-data.clusterdata_2019_a.instance_events`
job_id: bqjob_r22952b71577bfdac_000001a090a8aaef_1
bytes_processed: 54954173504
bytes_billed: 54954819584

| metric | value |
|---|---:|
| task_count | 80432291 |
| submitted_tasks | 80422758 |
| scheduled_tasks | 74556650 |
| terminal_tasks | 80208023 |
| valid_wait_tasks | 74532084 |
| valid_service_tasks | 74387565 |
| evict_events | 117133729 |
| fail_events | 17358057 |
| finish_events | 73611983 |
| kill_events | 149277877 |
| lost_events | 4351433 |

Wait quantiles are in seconds at percentiles 0, 1, ..., 100.
The schedule-to-terminal quantiles are lifecycle-envelope durations across possible retries/interruption, not per-attempt service times.

Boundary: remote observational aggregate; no controlled capacity intervention.
