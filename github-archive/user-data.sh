#!/bin/bash

NUM_NODES=__NUM_NODES__
CLUSTER_NAME="crate-github-demo"
QUORUM=$(($NUM_NODES/2+1))


echo "
export AWS_ACCESS_KEY_ID=__AWS_ACCESS_KEY_ID__
export AWS_SECRET_ACCESS_KEY=__AWS_SECRET_ACCESS_KEY__
export CRATE_HEAP_SIZE=15g
" >> /etc/sysconfig/crate

echo "
cluster.name: $CLUSTER_NAME
discovery.zen.minimum_master_nodes: $QUORUM

http.cors.enabled: true
gateway:
  recover_after_nodes: $QUORUM
  recover_after_time: 5m
  expected_nodes: $NUM_NODES
" >> /etc/crate/crate.yml

for u in chaudum mikethebeer kovrus ChrisChinchilla celaus joemoe; do
  /usr/bin/curl -w "\n" https://github.com/${u}.keys >> /home/ec2-user/.ssh/authorized_keys
done
