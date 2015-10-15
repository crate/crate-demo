CREATE TABLE github (
    type STRING,
    payload OBJECT(ignored),
    payload_push_event OBJECT(STRICT) AS (
        ref STRING,
        head STRING,
        size INTEGER,
        distinct_size INTEGER,
        commits ARRAY(OBJECT(STRICT) AS (
            id STRING,
            message STRING,
            "timestamp" TIMESTAMP,
            url STRING,
            author OBJECT(STRICT) AS (
                name STRING,
                email STRING,
                username STRING
            )
        ))
    ),
    payload_pull_request_event OBJECT(STRICT) AS (
        action STRING,
        "number" INTEGER,
        pull_request OBJECT(STRICT) AS (
            url STRING,
            id LONG,
            body STRING,
            title STRING,
            created_at TIMESTAMP,
            updated_at TIMESTAMP,
            merged_at TIMESTAMP,
            closed_at TIMESTAMP,
            head OBJECT(STRICT) AS (
                label STRING,
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
    ),
    repo OBJECT(STRICT) AS (
        id LONG,
        name STRING,
        url STRING,
        created_at TIMESTAMP,
        pushed_at TIMESTAMP,
        description STRING,
        homepage STRING,
        master_branch STRING,
        owner STRING,
        organization STRING,
        language STRING,
        size LONG,
        stargazers LONG
    ),
    record_ft STRING INDEX using fulltext,
    actor OBJECT(STRICT) AS (
        id LONG,
        login STRING,
        gravatar_id STRING,
        avatar_url STRING,
        url STRING,
        email STRING,
        company STRING,
        blog STRING,
        location STRING,
        type STRING,
        name STRING
    ),
    org OBJECT(STRICT) AS (
        id LONG,
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
