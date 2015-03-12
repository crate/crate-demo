-- Techcrunch Demo Queries

-- count all steps records
SELECT count(*) FROM steps;

-- count all steps
SELECT sum(num_steps) FROM steps;

-- count all steps for a specific user
SELECT sum(num_steps) AS steps_for_user FROM steps WHERE username = 'gosinski';

-- count all steps for a specific user on a specific month
SELECT sum(num_steps) AS steps_per_month FROM steps WHERE username = 'gosinski' AND month_partition = '201409';

-- histogram of daily steps for a specific user in a month
SELECT date_trunc('day', ts), sum(num_steps) FROM steps
  WHERE username = 'gosinski' AND month_partition = '201409'
  GROUP BY 1;

-- count all steps of all users on a specific day
SELECT date_trunc('day', ts), sum(num_steps) as num_steps, count(*) as num_records
  FROM steps
  WHERE month_partition = '201409'
  GROUP BY 1 ORDER BY 1 DESC;

-- count all steps for a specific user for each day
SELECT format('%tc', date_trunc('day', ts)) AS day, sum(num_steps) AS num_steps, count(*) AS num_records
  FROM steps
  WHERE username = 'gosinski'
  GROUP BY 1;

