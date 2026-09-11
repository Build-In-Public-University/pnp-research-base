# Google Borg BigQuery v4 results

status: remote_pressure_join_observation_24h
table: `google.com:google-cluster-data.clusterdata_2019_a.instance_events`
window: first 24 hours
job_id: bqjob_r61280c912a954735_000001a090d0e27e_1
bytes_processed: 54954173504
bytes_billed: 54954819584
result_rows: 100
missing_bucket_indices: [1]

| diagnostic | all buckets | excluding startup bucket 0 |
|---|---:|---:|
| bucket_count | 100 | 99 |
| submit_events | 3985691 | 2414050 |
| schedule_events | 3287210 | 2318605 |
| schedule_submit_ratio | 0.8247528471223685 | 0.9604627078975166 |
| closed_attempts | 2522119 | 2284633 |
| right_censored_attempts | 765091 | 33972 |
| peak_submit | (1571641, 0) | (86835, 91) |
| peak_schedule | (968605, 0) | (55491, 33) |
| peak_right_censored | (731119, 0) | (2524, 12) |
| median_bucket_p50_attempt_seconds | 388.958628 | 369.668255 |

The startup bucket is reported separately because it contains the opening state of the trace rather than a stationary interval.
Boundary: observational aggregate. The 96.0% schedule/submit ratio after excluding bucket 0 is descriptive, not causal evidence of adaptive headroom or queue migration.
