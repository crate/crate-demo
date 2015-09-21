#!/bin/sh

if [ "help" == "$1" ] ; then
  echo "usage: ./startscript <nr-instances> <key-name>"
  exit 1
else
    CountInstances=$1
fi

if [[ -z "$2" ]] ; then
  echo "Please specify a key-name"
  exit 1
fi

INSTANCE_IDS=$(bin/aws ec2 run-instances \
--image-id ami-358ba442 \
--count $CountInstances \
--instance-type c3.4xlarge \
--key-name $2 \
--user-data $(base64 user-data.sh) \
--block-device-mappings "[{\"DeviceName\":\"/dev/sdb\",\"VirtualName\":\"ephemeral0\"},{\"DeviceName\":\"/dev/sdc\",\"VirtualName\":\"ephemeral1\"}]" \
| jq ".Instances[].InstanceId" | tr -d '"')

echo "Instances launched"

bin/aws ec2 wait instance-exists --instance-ids $INSTANCE_IDS
echo "... existing"
bin/aws ec2 create-tags --resources $INSTANCE_IDS --tags Key=Name,Value=Crate-Github-Data
echo "... tagged"
bin/aws ec2 wait instance-status-ok --instance-ids $INSTANCE_IDS
echo "... ready"
