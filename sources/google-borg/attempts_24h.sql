WITH ordered AS (
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
  FROM `google.com:google-cluster-data.clusterdata_2019_a.instance_events`
  WHERE type IN (3, 4, 5, 6, 7, 8)
    AND time >= 0
    AND time < 86400000000
), attempts AS (
  SELECT
    collection_id,
    instance_index,
    attempt_no,
    MIN(IF(type = 3, time, NULL)) AS start_time,
    MIN(IF(type IN (4, 5, 6, 7, 8), time, NULL)) AS end_time,
    ARRAY_AGG(IF(type IN (4, 5, 6, 7, 8), type, NULL) IGNORE NULLS ORDER BY time, type LIMIT 1)[SAFE_OFFSET(0)] AS terminal_type,
    COUNTIF(type = 4) AS evict_events,
    COUNTIF(type = 5) AS fail_events,
    COUNTIF(type = 6) AS finish_events,
    COUNTIF(type = 7) AS kill_events,
    COUNTIF(type = 8) AS lost_events
  FROM ordered
  WHERE attempt_no > 0
  GROUP BY collection_id, instance_index, attempt_no
)
SELECT
  COUNT(*) AS attempt_count,
  COUNTIF(start_time IS NOT NULL) AS started_attempts,
  COUNTIF(end_time IS NOT NULL AND end_time >= start_time) AS closed_attempts,
  COUNTIF(end_time IS NULL) AS right_censored_attempts,
  COUNTIF(terminal_type = 4) AS evicted_attempts,
  COUNTIF(terminal_type = 5) AS failed_attempts,
  COUNTIF(terminal_type = 6) AS finished_attempts,
  COUNTIF(terminal_type = 7) AS killed_attempts,
  COUNTIF(terminal_type = 8) AS lost_attempts,
  SUM(evict_events) AS evict_events,
  SUM(fail_events) AS fail_events,
  SUM(finish_events) AS finish_events,
  SUM(kill_events) AS kill_events,
  SUM(lost_events) AS lost_events,
  APPROX_QUANTILES(IF(end_time IS NOT NULL AND end_time >= start_time, (end_time - start_time) / 1000000.0, NULL), 100) AS attempt_seconds_quantiles
FROM attempts;
