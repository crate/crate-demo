-- users
DROP TABLE users;
CREATE TABLE users (
    username STRING PRIMARY KEY,
    name STRING,
    address STRING INDEX USING FULLTEXT,
    date_of_birth TIMESTAMP,
    date_joined TIMESTAMP,
    month_partition STRING PRIMARY KEY
) CLUSTERED INTO 4 shards
  PARTITIONED BY (month_partition)
  WITH (number_of_replicas = 0, refresh_interval = 0);

-- steps
DROP TABLE steps;
CREATE TABLE steps (
    username STRING,
    ts TIMESTAMP,
    num_steps INTEGER,
    month_partition STRING,
    payload OBJECT(dynamic)
) CLUSTERED BY (username) INTO 4 shards
  PARTITIONED BY (month_partition)
  WITH (number_of_replicas = 0, refresh_interval = 0);
