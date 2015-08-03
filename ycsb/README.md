# YCSB Cluster Setup

## Bootstrapping

```console
$ python bootstrap.py
$ bin/buildout -N
```

## Launch Cluster

```console
$ ./launch --num-instances [1,2,4,8,16,32]
```

## Public/Private DNS

Load instance DNS names into dsh group:

```console
$ bin/aws ec2 describe-instances --filters Name=key-name,Values=ycsb Name=instance-state-name,Values=running Name=instance-type,Values=i2.xlarge | jq ".Reservations[].Instances[].PublicDnsName" | tr -d '\"' > ~/.dsh/group/ycsb8
```

To obtain the private IPs for the client nodes:

```console
$  bin/aws ec2 describe-instances --filters Name=key-name,Values=ycsb Name=instance-state-name,Values=running Name=instance-type,Values=i2.xlarge | jq ".Reservations[].Instances[].PrivateIpAddress" | tr -d '\"'
```

Run command via dsh, e.g.:

```console
$ dsh -g ycsb8 uptime
```

##Running workloads

#Loding the workload

```
./bin/ycsb load crate -s -P workloads/workloada -P crate.properties -P workload.properties -threads 40 -p insertstart=0 -p insertcount=2250000 > loada1.txt

./bin/ycsb load crate -s -P workloads/workloada -P crate.properties -P workload.properties  -threads 40 -p insertstart=2250000 -p insertcount=4500000 > loada2.txt

./bin/ycsb load crate -s -P workloads/workloada -P crate.properties -P workload.properties -threads 40 -p insertstart=4500000 -p insertcount=6750000 > loada3.txt

./bin/ycsb load crate -s -P workloads/workloada -P crate.properties -P workload.properties  -threads 40 -p insertstart=6750000 -p insertcount=9000000 > loada4.txt
```




