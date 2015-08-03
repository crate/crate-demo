#!/bin/bash -e

function print_red() {
  echo -e "\033[1;31m$1\033[0m"
}

function print_yellow() {
  echo -e "\033[2;33m$1\033[0m"
}

function print_green() {
  echo -e "\033[2;32m$1\033[0m"
}


while [[ $# > 1 ]]
do
key="$1"

case $key in
    -n|--num-instances)
    NUM_NODES="$2"
    shift
    ;;
    *)
            # unknown option
    ;;
esac
shift
done


if [ "x$NUM_NODES" = "x" ] ; then
  print_red "$0 requires argument: --num-instances <NUMBER_OF_NODES>"
  exit 1
else
  print_green "Launching $NUM_NODES instances."
fi

if `which jq >/dev/null` ; then
  print_green "jq is installed."
else
  print_red "jq (http://stedolan.github.io/jq/download/) needs to be installed!"
fi


CRATE_AMI="ami-e0fda997";
INSTANCE_TYPE="i2.xlarge"
SECURITY_GROUP="cluster$NUM_NODES"
AVAIL_ZONE="eu-west-1a"
KEY_NAME="ycsb"

USER_DATA="user-data-${NUM_NODES}.sh"
sed "s/__NUM_NODES__/$NUM_NODES/" user-data.sh > $USER_DATA

bin/aws ec2 run-instances \
  --count $NUM_NODES \
  --image-id $CRATE_AMI \
  --instance-type $INSTANCE_TYPE \
  --security-groups $SECURITY_GROUP \
  --placement AvailabilityZone=$AVAIL_ZONE \
  --key-name $KEY_NAME \
  --block-device-mappings "[{\"DeviceName\": \"/dev/sdb\", \"VirtualName\": \"ephemeral0\"}]" \
  --user-data $(cat $USER_DATA | base64)

