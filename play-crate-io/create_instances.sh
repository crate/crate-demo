#!/bin/bash

ZONE="us-central1-b"
PROJECT="<PROJECT_ID>"
NETWORK="play"

for i in {1..8}
do
    NODE="play${i}"
    DISK="ssd-${NODE}"

    # create disk
    echo "Create disk $DISK ..."

    gcloud compute disks create $DISK \
           --project $PROJECT \
           --zone $ZONE \
           --type pd-ssd \
           --size 50GB

    # create instance
    echo "Create instance $NODE ..."

    gcloud compute instances create $NODE \
           --project $PROJECT \
           --network $NETWORK \
           --image coreos \
           --machine-type n1-standard-8 \
           --zone $ZONE \
           --disk name=$DISK \
           --metadata-from-file user-data=cloud-config.yaml

done
