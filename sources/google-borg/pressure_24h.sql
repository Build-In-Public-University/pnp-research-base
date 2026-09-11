WITH base AS (
  SELECT
    collection_id,
    instance_index,
    time,
    type,
    DIV(time, 300000000) AS bucket_5m
  FROM `google.com:google-cluster-data.clusterdata_2019_a.instance_events`
  WHERE type IN (0, 3, 4, 5, 6, 7, 8)
    AND time >= 0
    AND time < 86400000000
), event_buckets AS (
  SELECT
    bucket_5m,
    COUNTIF(type = 0) AS submit_events,
    COUNTIF(type = 3) AS schedule_events,
    COUNTIF(type = 4) AS evict_events,
    COUNTIF(type = 5) AS fail_events,
    COUNTIF(type = 6) AS finish_events,
    COUNTIF(type = 7) AS kill_events,
    COUNTIF(type = 8) AS lost_events
  FROM base
  GROUP BY bucket_5m
), numbered AS (
  SELECT
    collection_id,
    instance_index,
    time,
    type,
    SUM(IF(type = 3, 1, 0)) OVER (
      PARTITION BY collection_id, instance_index
      ORDER BY time, type
      ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS attempt_no
  FROM base
  WHERE type IN (3, 4, 5, 6, 7, 8)
), attempts AS (
  SELECT
    collection_id,
    instance_index,
    attempt_no,
    MIN(IF(type = 3, time, NULL)) AS start_time,
    MIN(IF(type IN (4, 5, 6, 7, 8), time, NULL)) AS end_time,
    ARRAY_AGG(IF(type IN (4, 5, 6, 7, 8), type, NULL) IGNORE NULLS ORDER BY time, type LIMIT 1)[SAFE_OFFSET(0)] AS terminal_type
  FROM numbered
  WHERE attempt_no > 0
  GROUP BY collection_id, instance_index, attempt_no
), attempt_buckets AS (
  SELECT
    DIV(start_time, 300000000) AS bucket_5m,
    COUNT(*) AS started_attempts,
    COUNTIF(end_time IS NOT NULL AND end_time >= start_time) AS closed_attempts,
    COUNTIF(end_time IS NULL) AS right_censored_attempts,
    COUNTIF(terminal_type = 4) AS evicted_attempts,
    COUNTIF(terminal_type = 5) AS failed_attempts,
    COUNTIF(terminal_type = 6) AS finished_attempts,
    COUNTIF(terminal_type = 7) AS killed_attempts,
    COUNTIF(terminal_type = 8) AS lost_attempts,
    AVG(IF(end_time IS NOT NULL AND end_time >= start_time, (end_time - start_time) / 1000000.0, NULL)) AS mean_attempt_seconds,
    APPROX_QUANTILES(IF(end_time IS NOT NULL AND end_time >= start_time, (end_time - start_time) / 1000000.0, NULL), 100)[SAFE_OFFSET(50)] AS p50_attempt_seconds,
    APPROX_QUANTILES(IF(end_time IS NOT NULL AND end_time >= start_time, (end_time - start_time) / 1000000.0, NULL), 100)[SAFE_OFFSET(90)] AS p90_attempt_seconds
  FROM attempts
  GROUP BY bucket_5m
)
SELECT
  e.bucket_5m,
  e.submit_events,
  e.schedule_events,
  e.evict_events,
  e.fail_events,
  e.finish_events,
  e.kill_events,
  e.lost_events,
  COALESCE(a.started_attempts, 0) AS started_attempts,
  COALESCE(a.closed_attempts, 0) AS closed_attempts,
  COALESCE(a.right_censored_attempts, 0) AS right_censored_attempts,
  COALESCE(a.evicted_attempts, 0) AS evicted_attempts,
  COALESCE(a.failed_attempts, 0) AS failed_attempts,
  COALESCE(a.finished_attempts, 0) AS finished_attempts,
  COALESCE(a.killed_attempts, 0) AS killed_attempts,
  COALESCE(a.lost_attempts, 0) AS lost_attempts,
  a.mean_attempt_seconds,
  a.p50_attempt_seconds,
  a.p90_attempt_seconds
FROM event_buckets e
LEFT JOIN attempt_buckets a USING (bucket_5m)
ORDER BY e.bucket_5m;
