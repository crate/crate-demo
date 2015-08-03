#!/bin/bash
TASK=$1
WORKLOAD=$2

if [ "x$WORKLOAD" = "x" ] ; then
  echo "$0 requires 2 arguments: task [load|run] workload [a,b,c,d]"
  exit 1
fi

NODES=8
DIR="out/$NODESnodes/workload$WORKLOAD"
NODE=$(hostname)
ycsb $TASK crate -s \
  -threads 40 \
  -P workloads/workload$WORKLOAD \
  -P crate.properties \
  -P workload.properties \
  -P run.properties > "$DIR/$1-${NODE}.txt"

