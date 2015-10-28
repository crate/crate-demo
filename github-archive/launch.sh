#!/bin/sh -e

if [ "help" == "$1" ] ; then
  echo "usage: ./startscript <nr-nodes> <key-name> <ami-id>"
  exit 1
else
    NUM_NODES=$1
fi

if [[ -z "$2" ]] ; then
  echo "Please specify a key-name"
  exit 1
fi

if [[ -z "$3" ]] ; then
  echo "Please specify an ami-id"
  exit 1
fi

if [ ".$AWS_ACCESS_KEY_ID" = "." ] || [ ".$AWS_SECRET_ACCESS_KEY" = "." ] ; then
    echo "Please specify an AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY\n"
    echo "usage:"
    echo "export AWS_ACCESS_KEY_ID=<YOUR_ACCESS_KEY_ID>"
    echo "export AWS_SECRET_ACCESS_KEY=<YOUR_SECRET_ACCESS_KEY>"
    exit 1
fi

function sed_replace() {
  # require all 3 parameters
  if [ ".$1" = "." ] || [ ".$2" = "." ] || [ ".$3" = "." ] ; then
    echo "Usage: $0 [oldString] [newString] [targetFile]"
    echo $1 $2 $3
    exit 1
  fi
  local oldString="$1"
  local newString="$2"
  local targetFile="$3"
  local temp=$(mktemp -t sed_replace.XXXXXXXXX)
  chmod ug+rw $temp
  sed 's#'"$oldString"'#'"$newString"'#g' $targetFile > $temp
  mv $temp $targetFile
}

sed_replace "NUM_NODES=.*" "NUM_NODES=$NUM_NODES" user-data.sh
sed_replace "AWS_ACCESS_KEY_ID=.*" "AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID" user-data.sh
sed_replace "AWS_SECRET_ACCESS_KEY=.*" "AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY" user-data.sh

INSTANCE_TYPE="c3.4xlarge"
SECURITY_GROUP="github-demo"
REGION="us-west-2"


INSTANCE_IDS=$(bin/aws ec2 run-instances \
--image-id $3 \
--count $NUM_NODES \
--instance-type $INSTANCE_TYPE \
--key-name $2 \
--security-groups $SECURITY_GROUP \
--region $REGION \
--user-data $(base64 user-data.sh) \
--block-device-mappings "[{\"DeviceName\":\"/dev/sdb\",\"VirtualName\":\"ephemeral0\"},{\"DeviceName\":\"/dev/sdc\",\"VirtualName\":\"ephemeral1\"}]" \
| jq ".Instances[].InstanceId" | tr -d '"')

echo "Cluster launched with $NUM_NODES nodes"

bin/aws ec2 wait instance-exists --instance-ids $INSTANCE_IDS
echo "... existing"
bin/aws ec2 create-tags --resources $INSTANCE_IDS --tags Key=Name,Value=Crate-Github-Data
echo "... tagged"
bin/aws ec2 wait instance-status-ok --instance-ids $INSTANCE_IDS
echo "... ready"
