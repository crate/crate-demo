#!/bin/bash

NUM_NODES=16
CLUSTER_NAME="crate-github-demo"
GROUP="cluster-github"
QUORUM=$(($NUM_NODES/2+1))

echo "
export AWS_ACCESS_KEY_ID=''
export AWS_SECRET_ACCESS_KEY=''
export CRATE_HEAP_SIZE=15g
" >> /etc/sysconfig/crate

echo "
cluster.name: crate-$NUM_NODES
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
discovery.zen.ping.multicast.enabled: false
discovery:
  type: ec2
  zen:
    minimum_master_nodes: $QUORUM
  ec2:
    groups: $GROUP
http.cors.enabled: true
insert_by_query.request_timeout: 2m
gateway:
  recover_after_nodes: $QUORUM
  recover_after_time: 5m
  expected_nodes: $NUM_NODES
" >> /etc/crate/crate.yml
