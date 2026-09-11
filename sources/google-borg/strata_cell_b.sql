WITH base AS (
  SELECT
    collection_id,
    instance_index,
    time,
    type,
    scheduling_class,
    priority,
    collection_type,
    resource_request.cpus AS request_cpus,
    resource_request.memory AS request_memory
  FROM `google.com:google-cluster-data.clusterdata_2019_b.instance_events`
  WHERE type IN (3, 4, 5, 6, 7, 8)
    AND time >= 0
    AND time < 86400000000
), numbered AS (
  SELECT
    *,
    SUM(IF(type = 3, 1, 0)) OVER (
      PARTITION BY collection_id, instance_index
      ORDER BY time, type
      ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS attempt_no
  FROM base
), attempts AS (
  SELECT
    collection_id,
    instance_index,
    attempt_no,
    MIN(IF(type = 3, time, NULL)) AS start_time,
    MIN(IF(type IN (4, 5, 6, 7, 8), time, NULL)) AS end_time,
    ARRAY_AGG(IF(type IN (4, 5, 6, 7, 8), type, NULL) IGNORE NULLS ORDER BY time, type LIMIT 1)[SAFE_OFFSET(0)] AS terminal_type,
    ARRAY_AGG(IF(type = 3, STRUCT(scheduling_class, priority, collection_type, request_cpus, request_memory), NULL) IGNORE NULLS ORDER BY time LIMIT 1)[SAFE_OFFSET(0)] AS start_meta
  FROM numbered
  WHERE attempt_no > 0
  GROUP BY collection_id, instance_index, attempt_no
), classified AS (
  SELECT
    *,
    start_meta.scheduling_class AS scheduling_class,
    start_meta.priority AS priority,
    start_meta.collection_type AS collection_type,
    CASE
      WHEN start_meta.request_cpus IS NULL THEN 'missing'
      WHEN start_meta.request_cpus <= 0.1 THEN '<=0.1'
      WHEN start_meta.request_cpus <= 1 THEN '0.1-1'
      WHEN start_meta.request_cpus <= 4 THEN '1-4'
      ELSE '>4'
    END AS cpu_request_bin,
    CASE
      WHEN start_meta.request_memory IS NULL THEN 'missing'
      WHEN start_meta.request_memory <= 1 THEN '<=1'
      WHEN start_meta.request_memory <= 4 THEN '1-4'
      WHEN start_meta.request_memory <= 16 THEN '4-16'
      ELSE '>16'
    END AS memory_request_bin
  FROM attempts
  WHERE start_time IS NOT NULL
)
SELECT
  scheduling_class,
  priority,
  collection_type,
  cpu_request_bin,
  memory_request_bin,
  COUNT(*) AS started_attempts,
  COUNTIF(end_time IS NOT NULL AND end_time >= start_time) AS closed_attempts,
  COUNTIF(end_time IS NULL) AS right_censored_attempts,
  COUNTIF(terminal_type = 4) AS evicted_attempts,
  COUNTIF(terminal_type = 5) AS failed_attempts,
  COUNTIF(terminal_type = 6) AS finished_attempts,
  COUNTIF(terminal_type = 7) AS killed_attempts,
  COUNTIF(terminal_type = 8) AS lost_attempts,
  APPROX_QUANTILES(IF(end_time IS NOT NULL AND end_time >= start_time, (end_time - start_time) / 1000000.0, NULL), 100)[SAFE_OFFSET(50)] AS p50_attempt_seconds,
  APPROX_QUANTILES(IF(end_time IS NOT NULL AND end_time >= start_time, (end_time - start_time) / 1000000.0, NULL), 100)[SAFE_OFFSET(90)] AS p90_attempt_seconds
FROM classified
GROUP BY scheduling_class, priority, collection_type, cpu_request_bin, memory_request_bin
ORDER BY started_attempts DESC;
