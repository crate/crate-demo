-- which are the most sedimental months?

SELECT date_format('%Y-%m', date_trunc('month', created_at)) AS date,
       count(*) AS cnt_pos
FROM github
WHERE match(payload_ft, 'yes hallelujah hurray bingo  amused cheerful excited glad proud')
  AND TYPE = 'PushEvent'
  AND (created_at >= '2013-01-01' AND created_at <= '2013-12-31')
GROUP BY date
ORDER BY date ASC;


SELECT date_format('%Y-%m', date_trunc('month', created_at)) AS date,
       count(*) AS cnt_neg
FROM github
WHERE match(payload_ft, 'argh angry annoyed annoying appalled bitter cranky hate hating mad')
  AND TYPE = 'PushEvent'
  AND (created_at >= '2013-01-01' AND created_at <= '2013-12-31')
GROUP BY date
ORDER BY date ASC;
