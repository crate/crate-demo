#!/bin/bash

NUM_NODES=__NUM_NODES__
CLUSTER_NAME="crate-github-demo-$NUM_NODES"
GROUP="github-demo"
QUORUM=$(($NUM_NODES/2+1))


echo "
export AWS_ACCESS_KEY_ID=__AWS_ACCESS_KEY_ID__
export AWS_SECRET_ACCESS_KEY=__AWS_SECRET_ACCESS_KEY__
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

for u in chaudum mikthebeer kovrus ChrisChinchilla celaus; do
  /usr/bin/curl -w "\n" https://github.com/${u}.keys >> /home/ec2-user/.ssh/authorized_keys
done
