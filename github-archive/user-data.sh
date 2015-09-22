#!/bin/bash

NUM_NODES=16
CLUSTER_NAME="crate-github-demo"
GROUP="github-demo"
QUORUM=$(($NUM_NODES/2+1))

echo "
export AWS_ACCESS_KEY_ID=''
export AWS_SECRET_ACCESS_KEY=''
export CRATE_HEAP_SIZE=15g
" >> /etc/sysconfig/crate

echo "
cluster.name: $CLUSTER_NAME
index.store.type: mmapfs
indices:
  store:
    throttle:
      max_bytes_per_sec: 200mb
  recovery:
    max_bytes_per_sec: 200mb
    concurrent_streams: 5
  memory:
    index_buffer_size: 30%

discovery.ec2.groups: $GROUP
discovery.zen.minimum_master_nodes: $QUORUM

http.cors.enabled: true
insert_by_query.request_timeout: 2m
gateway:
  recover_after_nodes: $QUORUM
  recover_after_time: 5m
  expected_nodes: $NUM_NODES
" >> /etc/crate/crate.yml
