-- some PR latencys (time diff between created and merged)

select count(DISTINCT(repo['id'])) as cnt,
run(avg((extract (day from (payload['pull_request']['merged_at']-payload['pull_request']['created_at']))*24*60*60+
extract (hour from (payload['pull_request']['merged_at']-payload['pull_request']['created_at']))*60*60+
extract (minute from (payload['pull_request']['merged_at']-payload['pull_request']['created_at']))*60+
extract (second from (payload['pull_request']['merged_at']-payload['pull_request']['created_at'])))/3600)) as avg_diff,
date_format('%Y-%m-%d', payload['pull_request']['created_at']) as created_at
from github
where payload['pull_request']['created_at'] >= '2015-01-01' 
and payload['pull_request']['created_at'] <= '2015-01-30'
and payload['pull_request']['created_at'] is not null
and payload['pull_request']['merged_at'] is not null
and payload['pull_request']['head']['repo']['full_name'] is not null
group by created_at
order by created_at desc;
