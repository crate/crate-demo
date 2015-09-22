-- which are the most sedimental months?

select 
date_format('%Y-%m', date_trunc('month', created_at)) as date, 
count(*)
from github 
where '%yes%' like any (payload['commits']['message'])
or '%hallelujah%' like any (payload['commits']['message'])
or '%hurray%' like any (payload['commits']['message'])
or '%bingo%' like any (payload['commits']['message'])
or '%amused%' like any (payload['commits']['message'])
or '%cheerful%' like any (payload['commits']['message'])
or '%excited%' like any (payload['commits']['message'])
or '%glad%' like any (payload['commits']['message'])
or '%proud%' like any (payload['commits']['message']) 
group by date 
order by date desc;

select 
date_format('%Y-%m', date_trunc('month', created_at)) as date, 
count(*)
from github 
where '%no%' like any (payload['commits']['message'])
or '%fuck%' like any (payload['commits']['message'])
or '%shit%' like any (payload['commits']['message'])
or '%damn%' like any (payload['commits']['message'])
or '%stupid%' like any (payload['commits']['message'])
or '%bitch%' like any (payload['commits']['message']) 
group by date 
order by date desc;
