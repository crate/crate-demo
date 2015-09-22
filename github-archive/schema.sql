CREATE TABLE github (
    type STRING,
    payload OBJECT AS(
      commits OBJECT AS (
        message STRING
      )
    ),
    repo OBJECT,
    actor OBJECT,
    org OBJECT,
    created_at TIMESTAMP,
    month_partition STRING,
    id STRING,
    public BOOLEAN,
    INDEX commit_comment_ft using fulltext(payload['commits']['message']) with (analyzer = 'english')
    ) PARTITIONED BY (month_partition)
    WITH (number_of_replicas=0,
            refresh_interval=0);
