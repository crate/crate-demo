CREATE TABLE github (
    type STRING,
    payload OBJECT(STRICT) AS (
        push_event OBJECT(STRICT) AS (
            ref STRING,
            head STRING,
            before STRING,
            size INTEGER,
            distinct_size INTEGER,
            commits ARRAY(OBJECT(STRICT) AS (
                id STRING,
                message STRING,
                "distinct" BOOLEAN,
                "timestamp" TIMESTAMP,
                url STRING,
                author OBJECT(STRICT) AS (
                    name STRING,
                    email STRING,
                    username STRING
                ),
                commiter OBJECT(STRICT) AS (
                    name STRING,
                    email STRING,
                    username STRING
                )
            ))
        ),
        pull_request_event OBJECT(STRICT) AS (
            action STRING,
            "number" INTEGER,
            pull_request OBJECT(STRICT) AS (
                url STRING,
                id LONG,
                title STRING,
                body STRING,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                merged_at TIMESTAMP,
                closed_at TIMESTAMP,
                head OBJECT(STRICT) AS (
                    label STRING,
                    ref STRING,
                    sha STRING,
                    repo OBJECT(STRICT) AS (
                        id LONG,
                        name STRING,
                        full_name STRING,
                        language STRING,
                        description STRING,
                        created_at TIMESTAMP,
                        updated_at TIMESTAMP,
                        merged_at TIMESTAMP
                    )
                )
            )
        )
    ),
    repo OBJECT(STRICT) AS (
        id INTEGER,
        name STRING,
        url STRING
    ),
    payload_ft STRING INDEX using fulltext,
    actor OBJECT(STRICT) AS (
        id INTEGER,
        login STRING,
        gravatar_id STRING,
        avatar_url STRING,
        url STRING
    ),
    org OBJECT(STRICT) AS (
        id INTEGER,
        login STRING,
        gravatar_id STRING,
        avatar_url STRING,
        url STRING
    ),
    created_at TIMESTAMP,
    month_partition STRING,
    id STRING,
    public BOOLEAN
) PARTITIONED BY (month_partition)
WITH (
    number_of_replicas = 1,
    refresh_interval = 0
);
