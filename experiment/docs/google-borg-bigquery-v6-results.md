# Google Borg BigQuery v6 results

status: cross-cell observational replication
window: first 24 hours; startup bucket 0 excluded from correlations

| metric | cell a | cell b |
|---|---:|---:|
| attempts | 7820880 | 9301457 |
| closed attempts | 6646807 | 8561541 |
| right-censored attempts | 1174073 | 739916 |
| attempt p50 seconds | 362.55466 | 315.439397 |
| attempt p90 seconds | 4366.2881 | 4728.397513 |
| attempt p99 seconds | 44717.532258 | 49879.379297 |
| schedule/submit ratio | 0.9604627078975166 | 0.9759475090853033 |
| peak CPU proxy | 0.7037581472843258 | 0.8286715719582514 |
| peak memory proxy | 0.8835161202479987 | 1.185674548160424 |
| submit vs CPU correlation | 0.23796729849303558 | -0.13421478924325267 |
| submit vs memory correlation | 0.2348466166034434 | 0.5016325700636777 |
| schedule vs CPU correlation | 0.13280183566721343 | -0.10599160402196864 |
| schedule vs memory correlation | 0.18854248037640836 | 0.5200187294360835 |
| p50 duration vs CPU correlation | -0.214806178985045 | -0.11213461500480769 |
| p50 duration vs memory correlation | -0.24308095207247749 | 0.06971616102635086 |

Cell b changes the sign and magnitude of several associations. Memory association with submits/schedules is stronger in cell b, while CPU association becomes slightly negative. This is evidence of cross-cell heterogeneity, not a universal mechanism.
The memory proxy exceeds 1 in cell b; it is not physical utilization.
