# Google Borg BigQuery v5 results

status: remote_capacity_usage_join_observation_24h
window: first 24 hours; bucket 0 excluded from correlations
pressure_job: bqjob_r61280c912a954735_000001a090d0e27e_1
usage_job: bqjob_r3fafe877ddfa5dc4_000001a090d8b5dd_1
pressure_bytes_processed: 54954173504
usage_bytes_processed: 242417123288

| pressure metric | CPU correlation | memory correlation |
|---|---:|---:|
| submit_events | 0.2379673 | 0.23484662 |
| schedule_events | 0.13280184 | 0.18854248 |
| closed_attempts | 0.14171128 | 0.19665148 |
| right_censored_attempts | -0.15988217 | -0.1221266 |
| p50_attempt_seconds | -0.21480618 | -0.24308095 |

joined buckets: 99
peak CPU proxy: (0.7037581472843258, 7)
peak memory proxy: (0.8835161202479987, 38)
peak submits: (86835.0, 91)
peak p50 attempt seconds: (820.240824, 3)

Interpretation: the association is weak and non-monotone. This does not establish that resource saturation caused the observed pressure pattern, nor does it falsify queue migration.
