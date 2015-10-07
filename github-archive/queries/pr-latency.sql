-- some PR latencys (time diff between created and merged)

SELECT count(DISTINCT(repo['id'])) AS cnt,
       round(avg((extract(day from (payload['pull_request_event']['pull_request']['merged_at'] - payload['pull_request_event']['pull_request']['created_at'])) * 24 * 60 * 60 +
       extract(hour from (payload['pull_request_event']['pull_request']['merged_at'] - payload['pull_request_event']['pull_request']['created_at'])) * 60 * 60 +
       extract(minute from (payload['pull_request_event']['pull_request']['merged_at'] - payload['pull_request_event']['pull_request']['created_at'])) * 60 +
       extract(second from (payload['pull_request_event']['pull_request']['merged_at'] - payload['pull_request_event']['pull_request']['created_at']))) / 3600)) AS avg_diff,
       CAST(date_format('%', payload['pull_request_event']['pull_request']['created_at']) AS INTEGER) AS created_at
FROM github
WHERE payload['pull_request_event']['pull_request']['created_at'] >= '2011-01-01'
AND payload['pull_request_event']['pull_request']['created_at'] <= '2011-12-31'
AND payload['pull_request_event']['pull_request']['created_at'] IS NOT NULL
AND payload['pull_request_event']['pull_request']['merged_at'] IS NOT NULL
GROUP BY created_at
ORDER BY created_at ASC
