create table uservisits (
    "sourceIP" string,
    "destinationURL" string,
    "visitDate" timestamp,
    "adRevenue" float,
    "UserAgent" string INDEX using fulltext,
    "cCode" string,
    "lCode" string,
    "searchWord" string,
    "duration" int
) clustered into 96 shards with (number_of_replicas = 0, refresh_interval = 0);
