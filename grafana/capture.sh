#!/bin/bash
url='http://localhost:4200/_sql?pretty'

function schema() {
curl -sSXPOST $url -d@- <<- EOF
{
  "stmt":
    "CREATE TABLE IF NOT EXISTS \"stats\".\"nodes\" (
      \"ts\" TIMESTAMP,
      \"week_partition\" as date_format('%x%v', ts),
      \"id\" STRING,
      \"name\" STRING,
      \"hostname\" STRING,
      \"rest_url\" STRING,
      \"port\" OBJECT(strict) AS (
        \"http\" INTEGER,
        \"transport\" INTEGER
      ),
      \"load\" OBJECT(strict) AS (
        \"1\" DOUBLE,
        \"5\" DOUBLE,
        \"15\" DOUBLE,
        \"probe_timestamp\" TIMESTAMP
      ),
      \"mem\" OBJECT(strict) AS (
        \"free\" LONG,
        \"used\" LONG,
        \"free_percent\" SHORT,
        \"used_percent\" SHORT,
        \"probe_timestamp\" TIMESTAMP
      ),
      \"heap\" OBJECT(strict) AS (
        \"free\" LONG,
        \"used\" LONG,
        \"max\" LONG,
        \"probe_timestamp\" TIMESTAMP
      ),
      \"version\" OBJECT(strict) AS (
        \"number\" STRING,
        \"build_hash\" STRING,
        \"build_snapshot\" BOOLEAN
      ),
      \"thread_pools\" ARRAY(
        OBJECT(strict) AS (
          \"name\" STRING,
          \"active\" INTEGER,
          \"rejected\" LONG,
          \"largest\" INTEGER,
          \"completed\" LONG,
          \"threads\" INTEGER,
          \"queue\" INTEGER
        )
      ),
      \"network\" OBJECT(strict) AS (
        \"probe_timestamp\" TIMESTAMP,
        \"tcp\" OBJECT(strict) AS (
          \"connections\" OBJECT(strict) AS (
            \"initiated\" LONG,
            \"accepted\" LONG,
            \"curr_established\" LONG,
            \"dropped\" LONG,
            \"embryonic_dropped\" LONG
          ),
          \"packets\" OBJECT(strict) AS (
            \"sent\" LONG,
            \"received\" LONG,
            \"retransmitted\" LONG,
            \"errors_received\" LONG,
            \"rst_sent\" LONG
          )
        )
      ),
      \"os\" OBJECT (strict) AS (
        \"uptime\" LONG,
        \"timestamp\" TIMESTAMP,
        \"probe_timestamp\" TIMESTAMP,
        \"cpu\" OBJECT(strict) AS (
          \"system\" SHORT,
          \"user\" SHORT,
          \"idle\" SHORT,
          \"used\" SHORT,
          \"stolen\" SHORT
        )
      ),
      \"os_info\" OBJECT(strict) AS (
        \"available_processors\" INTEGER,
        \"name\" STRING,
        \"arch\" STRING,
        \"version\" STRING,
        \"jvm\" OBJECT(strict) AS (
          \"vm_name\" STRING,
          \"vm_vendor\" STRING,
          \"vm_version\" STRING,
          \"version\" STRING
        )
      ),
      \"process\" OBJECT(strict) AS (
        \"open_file_descriptors\" LONG,
        \"max_open_file_descriptors\" LONG,
        \"probe_timestamp\" TIMESTAMP,
        \"cpu\" OBJECT(strict) AS (
          \"percent\" SHORT,
          \"user\" LONG,
          \"system\" LONG
        )
      ),
      \"fs\" OBJECT(strict) AS (
        \"total\" OBJECT(strict) AS (
          \"size\" LONG,
          \"used\" LONG,
          \"available\" LONG,
          \"reads\" LONG,
          \"bytes_read\" LONG,
          \"writes\" LONG,
          \"bytes_written\" LONG
        ),
        \"disks\" ARRAY(
          OBJECT(strict) AS (
            \"dev\" STRING,
            \"size\" LONG,
            \"used\" LONG,
            \"available\" LONG,
            \"reads\" LONG,
            \"bytes_read\" LONG,
            \"writes\" LONG,
            \"bytes_written\" LONG
          )
        ),
        \"data\" ARRAY(
          OBJECT(strict) AS (
            \"dev\" STRING,
            \"path\" STRING
          )
        )
      )
    )
    CLUSTERED INTO 6 SHARDS
    PARTITIONED BY (\"week_partition\")
  "
}
EOF

}

schema
while true; do
curl -sSXPOST $url -d@- <<- EOF
{
  "stmt": "INSERT INTO \"stats\".\"nodes\"
      (\"ts\", \"id\", \"name\", \"hostname\", \"rest_url\", \"port\", \"load\", \"mem\", \"heap\", \"version\", \"thread_pools\", \"network\", \"os\", \"os_info\", \"process\", \"fs\")
      (SELECT CURRENT_TIMESTAMP, \"id\", \"name\", \"hostname\", \"rest_url\", \"port\", \"load\", \"mem\", \"heap\", \"version\", \"thread_pools\", \"network\", \"os\", \"os_info\", \"process\", \"fs\" FROM sys.nodes)"
}
EOF
date
sleep 10
done
