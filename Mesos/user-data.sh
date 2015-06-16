# gcloud compute instances create weave-{1..3} --project crate-gce --zone us-central1-a --machine-type n1-standard-4 --image centos-7 --boot-disk-type pd-ssd --boot-disk-size 12GB --metadata-from-file startup-script=user-data.sh

# Weave-1
# sudo weave launch

# Others
# sudo weave launch weave-1

# sudo weave status

# Get Crate running

# sudo weave run 10.0.1.1/24 -p 4300:4300 -p 4200:4200 crate:latest crate -Des.cluster.name=crate-weave -Des.network.bind_host=0.0.0.0 -Des.network.publish_host=_ethwe:ipv4_

# sudo weave run 10.0.1.2/24 -p 4300:4300 -p 4200:4200 crate:latest crate -Des.cluster.name=crate-weave -Des.network.bind_host=0.0.0.0 -Des.network.publish_host=_ethwe:ipv4_

# sudo weave run 10.0.1.3/24 -p 4300:4300 -p 4200:4200 crate:latest crate -Des.cluster.name=crate-weave -Des.network.bind_host=0.0.0.0 -Des.network.publish_host=_ethwe:ipv4_

# expose to local network with random ip address
# sudo weave expose 10.0.1.101/24

# Make it accessible to the outside world
# gcloud compute firewall-rules create allow-crate --project crate-gce --allow tcp:4200, tcp:4300 --source-ranges 0.0.0.0/0

#!/bin/bash
# update repos
yum update -y
# install docker
yum install -y docker
service docker start
# install weave
sudo curl --location --output /usr/sbin/weave https://github.com/zettio/weave/releases/download/latest_release/weave
sudo chmod a+x /usr/sbin/weave
sudo docker pull crate:latest
sudo docker pull zettio/weave:latest
