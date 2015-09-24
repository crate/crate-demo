CREATE TABLE github (
    type STRING,
    payload OBJECT AS (
      commits ARRAY(OBJECT AS (
        sha STRING,
        author OBJECT,
        message STRING,
        "distinct" BOOLEAN,
        url STRING
      ))
    ),
    repo OBJECT AS (
      id LONG
    ),
    actor OBJECT,
    org OBJECT,
    created_at TIMESTAMP,
    month_partition STRING,
    id STRING,
    public BOOLEAN
) PARTITIONED BY (month_partition)
WITH (
    number_of_replicas = 0,
    refresh_interval = 0
);
