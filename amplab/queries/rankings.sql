drop table rankings;
create table rankings (
    "pageURL" string primary key,
    "pageRank" int,
    "avgDuration" int
) clustered into 48 shards with (number_of_replicas=0, refresh_interval=0);
