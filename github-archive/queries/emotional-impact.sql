-- which are the most sedimental months?

select 
date_format('%Y-%m', date_trunc('month', created_at)) as date, 
count(*) as cnt_pos
from github 
where '% yes %' like any (payload['commits']['message'])
or '% hallelujah %' like any (payload['commits']['message'])
or '% hurray %' like any (payload['commits']['message'])
or '% bingo %' like any (payload['commits']['message'])
or '% amused %' like any (payload['commits']['message'])
or '% cheerful %' like any (payload['commits']['message'])
or '% excited %' like any (payload['commits']['message'])
or '% glad %' like any (payload['commits']['message'])
or '% proud %' like any (payload['commits']['message']) 
group by date 
order by date desc;

select 
date_format('%Y-%m', date_trunc('month', created_at)) as date, 
count(*) as cnt_neg
from github 
where '% a+rgh %' like any (payload['commits']['message'])
or '% angry %' like any (payload['commits']['message'])
or '% annoyed %' like any (payload['commits']['message'])
or '% annoying %' like any (payload['commits']['message'])
or '% appalled %' like any (payload['commits']['message'])
or '% bitter %' like any (payload['commits']['message']) 
or '% cranky %' like any (payload['commits']['message']) 
or '% hate %' like any (payload['commits']['message']) 
or '% hating %' like any (payload['commits']['message']) 
or '% mad %' like any (payload['commits']['message']) 
group by date 
order by date desc;
