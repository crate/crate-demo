-- TOP 20 languages used in pull requests in a descending order of their frequency

SELECT payload['pull_request_event']['pull_request']['head']['repo']['language'] AS LANGUAGE,
       count(*) AS num_pull_requests,
       count(distinct(repo['id'])) AS num_repos
FROM github
WHERE TYPE = 'PullRequestEvent'
  AND payload['pull_request_event']['pull_request']['head']['repo']['language'] IS NOT NULL
  AND repo['id'] IS NOT NULL
GROUP BY 1
ORDER BY 2 DESC LIMIT 10
