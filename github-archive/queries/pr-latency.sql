-- some PR latencys (time diff between created and merged)

select count(*) as cnt,
(extract (day from (payload['pull_request']['merged_at']-payload['pull_request']['created_at']))*24*60*60+
extract (hour from (payload['pull_request']['merged_at']-payload['pull_request']['created_at']))*60*60+
extract (minute from (payload['pull_request']['merged_at']-payload['pull_request']['created_at']))*60+
extract (second from (payload['pull_request']['merged_at']-payload['pull_request']['created_at'])))/3600 as diff,
date_format(payload['pull_request']['created_at']) as created_at,
date_format(payload['pull_request']['merged_at']) as merged_at
from github
where payload['pull_request']['created_at'] is not null
and payload['pull_request']['merged_at'] is not null
group by diff, created_at, merged_at
order by cnt desc, diff desc
limit 100;
