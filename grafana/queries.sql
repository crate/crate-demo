SELECT date_trunc('minute', ts) as time,
       sum(load['1']) as load
FROM "stats"."nodes"
WHERE time >= ?
  AND time <= ?
GROUP BY time
ORDER BY time ASC

# aggregation / overview
# example 1 - avg. load one
# parameters: time aggregation span ('minute')
SELECT date_trunc('minute', ts) as time, hostname, AVG(load['1'])
  FROM stats.nodes
  WHERE ts > 1464256320000 and ts < 1464256330000
  GROUP by time, hostname
  ORDER BY time
  LIMIT 10;
