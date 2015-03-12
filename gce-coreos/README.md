# Techcrunch Demo Cluster

The intention for this demo cluster was to show an app that tracks
people's steps over a long period of time (like Apple's Health app).

Every minute the accumulated number of steps is stored in the Crate
cluster. The data should be queried so you can create time based
graphs with the step count of users.

## Instances

To list instances you will need to have ``gcloud`` utils installed.

https://cloud.google.com/compute/docs/gcloud-compute/

    $ gcloud compute instances list
    +--------+---------------+---------+----------------+-----------------+
    | name   | zone          | status  | network-ip     | external-ip     |
    +--------+---------------+---------+----------------+-----------------+
    | demo1  | us-central1-a | RUNNING | 10.240.231.118 | 146.148.91.230  |
    +--------+---------------+---------+----------------+-----------------+
    | demo2  | us-central1-a | RUNNING | 10.240.207.10  | 146.148.90.74   |
    +--------+---------------+---------+----------------+-----------------+
    | demo3  | us-central1-a | RUNNING | 10.240.212.45  | 146.148.85.147  |
    +--------+---------------+---------+----------------+-----------------+
    | demo4  | us-central1-a | RUNNING | 10.240.234.90  | 130.211.118.52  |
    +--------+---------------+---------+----------------+-----------------+
    | demo5  | us-central1-a | RUNNING | 10.240.131.3   | 146.148.90.88   |
    +--------+---------------+---------+----------------+-----------------+
    | demo6  | us-central1-a | RUNNING | 10.240.230.245 | 146.148.62.203  |
    +--------+---------------+---------+----------------+-----------------+
    | demo7  | us-central1-a | RUNNING | 10.240.202.128 | 146.148.49.214  |
    +--------+---------------+---------+----------------+-----------------+
    | demo8  | us-central1-a | RUNNING | 10.240.138.242 | 146.148.78.105  |
    +--------+---------------+---------+----------------+-----------------+
    | demo9  | us-central1-a | RUNNING | 10.240.6.80    | 146.148.42.240  |
    +--------+---------------+---------+----------------+-----------------+
    | demo10 | us-central1-a | RUNNING | 10.240.145.20  | 146.148.45.36   |
    +--------+---------------+---------+----------------+-----------------+
    | demo11 | us-central1-a | RUNNING | 10.240.7.62    | 146.148.77.241  |
    +--------+---------------+---------+----------------+-----------------+
    | demo12 | us-central1-a | RUNNING | 10.240.59.164  | 107.178.211.236 |
    +--------+---------------+---------+----------------+-----------------+


## Create tables

    crash --hosts=146.148.91.230:4200 < schema.sql


## Import sampledata

Sampledata are distributed evenly on all nodes.

    crash --hosts=146.148.91.230:4200 < import.sql


## Run queries

    crash --hosts=146.148.49.214:4200 < queries.sql


## Create Network

    $ gcloud compute networks create demo

    $ gcloud compute firewall-rules create demo-internal \
        --network demo \
        --source-ranges 10.240.0.0/16 \
        --allow tcp udp icmp

    $ gcloud compute firewall-rules create demo-external \
        --network demo \
        --source-ranges 0.0.0.0/0 \
        --allow tcp:22 tcp:80 tpc:4200


## Create Disks

    $ gcloud compute disks create ssd-demo-${x} \
        --project crate-gce \
        --zone us-central1-a \
        --size 50GB \
        --type pd-ssd


## Create Cluster

Update discovery hash in ``cloud-config.yaml`` and then run:

    $ gcloud compute instances create demo-${x} \
        --project crate-gce \
        --zone us-standard1-a \
        --image coreos \
        --disk name=demo-ssd-${x} \
        --machine-type n1-standard-8 \
        --boot-disk-size 8GB \
        --network demo \
        --metadata-from-file user-data=cloud-config.yaml

## Create and Upload Sampledata

    $ python create_sampledata.py 5000

Will result in ~1.3 billion records based on 5000 users.

The sampledata are split into files, each containing data of 100 users,
and written to the folder ``out/``.

To import the data distribute the files evenly across all nodes in the cluster.
Simply use ``scp`` to copy them to the remote hosts into
``/mnt/data1/crate/sampledata``. ``/mnt/data1/crate`` is mounted as
``/data`` in the Crate docker container and can therefore be used for the import.

