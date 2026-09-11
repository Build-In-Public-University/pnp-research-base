WITH per_task AS (
  SELECT
    collection_id,
    instance_index,
    MIN(IF(type = 0, time, NULL)) AS submit_time,
    MIN(IF(type = 3, time, NULL)) AS schedule_time,
    MAX(IF(type IN (4, 5, 6, 7, 8), time, NULL)) AS terminal_time,
    COUNTIF(type = 4) AS evict_count,
    COUNTIF(type = 5) AS fail_count,
    COUNTIF(type = 6) AS finish_count,
    COUNTIF(type = 7) AS kill_count,
    COUNTIF(type = 8) AS lost_count
  FROM `google.com:google-cluster-data.clusterdata_2019_a.instance_events`
  WHERE type IN (0, 3, 4, 5, 6, 7, 8)
  GROUP BY collection_id, instance_index
)
SELECT
  COUNT(*) AS task_count,
  COUNTIF(submit_time IS NOT NULL) AS submitted_tasks,
  COUNTIF(schedule_time IS NOT NULL) AS scheduled_tasks,
  COUNTIF(terminal_time IS NOT NULL) AS terminal_tasks,
  COUNTIF(submit_time IS NOT NULL AND schedule_time IS NOT NULL AND schedule_time >= submit_time) AS valid_wait_tasks,
  COUNTIF(schedule_time IS NOT NULL AND terminal_time IS NOT NULL AND terminal_time >= schedule_time) AS valid_service_tasks,
  SUM(evict_count) AS evict_events,
  SUM(fail_count) AS fail_events,
  SUM(finish_count) AS finish_events,
  SUM(kill_count) AS kill_events,
  SUM(lost_count) AS lost_events,
  APPROX_QUANTILES(IF(submit_time IS NOT NULL AND schedule_time IS NOT NULL AND schedule_time >= submit_time, (schedule_time - submit_time) / 1000000.0, NULL), 100) AS wait_seconds_quantiles,
  APPROX_QUANTILES(IF(schedule_time IS NOT NULL AND terminal_time IS NOT NULL AND terminal_time >= schedule_time, (terminal_time - schedule_time) / 1000000.0, NULL), 100) AS service_seconds_quantiles
FROM per_task;
