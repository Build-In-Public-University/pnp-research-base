WITH machine_capacity AS (
  SELECT
    machine_id,
    MAX(capacity.cpus) AS cpu_capacity,
    MAX(capacity.memory) AS memory_capacity
  FROM `google.com:google-cluster-data.clusterdata_2019_a.machine_events`
  WHERE capacity.cpus IS NOT NULL AND capacity.memory IS NOT NULL
  GROUP BY machine_id
), usage_buckets AS (
  SELECT
    DIV(start_time, 300000000) AS bucket_5m,
    SUM(average_usage.cpus) AS cpu_usage_sum,
    SUM(average_usage.memory) AS memory_usage_sum,
    COUNT(DISTINCT machine_id) AS active_machine_samples
  FROM `google.com:google-cluster-data.clusterdata_2019_a.instance_usage`
  WHERE start_time >= 0 AND start_time < 86400000000
  GROUP BY bucket_5m
), capacity_total AS (
  SELECT SUM(cpu_capacity) AS cpu_capacity_total, SUM(memory_capacity) AS memory_capacity_total
  FROM machine_capacity
)
SELECT
  u.bucket_5m,
  u.cpu_usage_sum,
  u.memory_usage_sum,
  u.active_machine_samples,
  c.cpu_capacity_total,
  c.memory_capacity_total,
  SAFE_DIVIDE(u.cpu_usage_sum, c.cpu_capacity_total) AS cpu_utilization_proxy,
  SAFE_DIVIDE(u.memory_usage_sum, c.memory_capacity_total) AS memory_utilization_proxy
FROM usage_buckets u CROSS JOIN capacity_total c
ORDER BY u.bucket_5m;
