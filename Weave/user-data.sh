# sudo /usr/local/bin/weave run 10.0.1.1/24 -p 4300:4300 -p 4200:4200 crate:latest crate -Des.cluster.name=crate-weave -Des.network.bind_host=0.0.0.0 -Des.network.publish_host=_ethwe:ipv4_

# sudo /usr/local/bin/weave run 10.0.1.2/24 -p 4300:4300 -p 4200:4200 crate:latest crate -Des.cluster.name=crate-weave -Des.network.bind_host=0.0.0.0 -Des.network.publish_host=_ethwe:ipv4_

# sudo /usr/local/bin/weave run 10.0.1.3/24 -p 4300:4300 -p 4200:4200 crate:latest crate -Des.cluster.name=crate-weave -Des.network.bind_host=0.0.0.0 -Des.network.publish_host=_ethwe:ipv4_

# expose to local network with random ip address
# sudo /usr/local/bin/weave expose 10.0.1.101/24

# Make it accessible to the outside world
# gcloud compute firewall-rules create allow-crate --project crate-gce --allow tcp:4200, tcp:4300 --source-ranges 0.0.0.0/0

#!/bin/bash
# update repos
yum update -y
# install docker
yum install -y docker
service docker start
# install weave
sudo -i
curl --location --output /usr/local/bin/weave https://github.com/zettio/weave/releases/download/latest_release/weave
chmod a+x /usr/local/bin/weave
# Would be good to PATH this somehow
docker pull crate:latest
docker pull zettio/weave:latest
