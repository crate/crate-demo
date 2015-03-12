#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
NUM=0
QUEUE=""
MAX_NPROC=8 # default

function execute {
    $DIR/run_history.sh $1
}
function queue {
    QUEUE="$QUEUE $1"
    NUM=$(($NUM+1))
}
function regeneratequeue {
    OLDREQUEUE=$QUEUE
    QUEUE=""
    NUM=0
    for PID in $OLDREQUEUE
    do
        if [ -d /proc/$PID ] ; then
            QUEUE="$QUEUE $PID"
            NUM=$(($NUM+1))
        fi
    done
}
function checkqueue {
    OLDCHQUEUE=$QUEUE
    for PID in $OLDCHQUEUE
    do
        if [ ! -d /proc/$PID ] ; then
            regeneratequeue # at least one PID has finished
            break
        fi
    done
}


for name in $(find /mnt/data20/wikipedia_history/ -name '*wiki*xml*.bz2' -printf "%f\n" |sort)
do
    execute $name &
    PID=$!
    queue $PID
    while [ $NUM -ge $MAX_NPROC ]; do
        checkqueue
        sleep 0.4
    done
done
wait
