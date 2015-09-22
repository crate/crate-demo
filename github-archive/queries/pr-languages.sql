-- TOP 20 languages used in pull requests in a descending order of their frequency

SELECT payload['pull_request']['head']['repo']['language'] AS language,
       COUNT(*) AS num_pull_requests,
       COUNT(DISTINCT(repo['id'])) AS num_repos
FROM github
WHERE type = 'PullRequestEvent'
  AND payload['pull_request']['head']['repo']['language'] IS NOT NULL
GROUP BY 1
ORDER BY 2 DESC
LIMIT 20;
