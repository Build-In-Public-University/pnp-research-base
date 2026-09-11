# Google Borg BigQuery v3 results

status: remote_attempt_observation_24h
table: `google.com:google-cluster-data.clusterdata_2019_a.instance_events`
window: first 24 hours (0 <= time < 86,400,000,000 microseconds)
job_id: bqjob_r68b77b2930c479ac_000001a090bab656_1
bytes_processed: 54954173504
bytes_billed: 54954819584

| metric | value |
|---|---:|
| attempt_count | 7820880 |
| started_attempts | 7820880 |
| closed_attempts | 6646807 |
| right_censored_attempts | 1174073 |
| evicted_attempts | 1944056 |
| failed_attempts | 318146 |
| finished_attempts | 1400373 |
| killed_attempts | 2820796 |
| lost_attempts | 163436 |
| evict_events | 2016704 |
| fail_events | 531215 |
| finish_events | 1418345 |
| kill_events | 2959684 |
| lost_events | 226051 |

| attempt duration p50 (seconds) | 362.55466 |
| attempt duration p90 (seconds) | 4366.2881 |
| attempt duration p99 (seconds) | 44717.532258 |

Right-censored attempts are excluded from duration quantiles. Boundary: observational first-window aggregate; no controlled capacity intervention.
