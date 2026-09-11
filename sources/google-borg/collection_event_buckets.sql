SELECT
  DIV(time, 300000000) AS bucket_5m,
  COUNTIF(type = 0) AS submit_count,
  COUNTIF(type = 1) AS queue_count,
  COUNTIF(type = 2) AS enable_count,
  COUNTIF(type = 3) AS schedule_count,
  COUNTIF(type = 4) AS evict_count,
  COUNTIF(type = 5) AS fail_count,
  COUNTIF(type = 6) AS finish_count,
  COUNTIF(type = 7) AS kill_count,
  COUNTIF(type = 8) AS lost_count
FROM `google.com:google-cluster-data.clusterdata_2019_a.collection_events`
GROUP BY bucket_5m
ORDER BY bucket_5m;
