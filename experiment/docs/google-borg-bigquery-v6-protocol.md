# Google Borg BigQuery v6 protocol

Apply the frozen v3 attempt, v4 pressure, and v5 capacity/usage queries to Borg cell `b`, using the same first-24-hour window and excluding startup bucket 0 from cross-cell correlations. No thresholds, query structure, bucket size, or interpretation rule may be retuned after viewing cell-b output.

Cell `a` is the prior receipted observation. Cell `b` is the replication target. All raw rows remain in BigQuery; only aggregate results and job metadata are retained.
