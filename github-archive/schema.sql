CREATE TABLE github (
    type STRING,
    public BOOLEAN,
    payload OBJECT(ignored),
    repo OBJECT(dynamic) AS (
        id INTEGER,
        name STRING,
        url STRING
    ),
    actor OBJECT(dynamic) AS (
        id INTEGER,
        login STRING,
        gravatar_id STRING,
        avatar_url STRING,
        url STRING
    ),
    org OBJECT(dynamic) AS (
        id INTEGER,
        login STRING,
        gravatar_id STRING,
        avatar_url STRING,
        url STRING
    ),
    created_at TIMESTAMP,
    month_partition STRING,
    id STRING
    )
    PARTITIONED BY (month_partition)
    WITH (number_of_replicas=0,
            refresh_interval=0);
