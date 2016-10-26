=============
play.crate.io
=============

Setup Cluster
-------------

This setup requires `Google Cloud SDK`_ to be installed!

Network/Firewall
................
*Only required if deleted*

Docs: `GCE Networking`_

Create a new network named ``play`` (or likewise)::

  $ gcloud compute networks create play

Allow internal traffic between instances, use IPv4 range from the
``gcloud compute networks list`` command for the ``--source-ranges`` parameter::

  $ gcloud compute firewall-rules create internal \
      --network play \
      --source-ranges 10.240.0.0/16 \
      --allow tcp udp icmp

Allow SSH connections and web traffic from everywhere::

  $ gcloud compute firewall-rules create web \
      --network play \
      --source-ranges 0.0.0.0/32 \
      --allow tcp:22 tcp:80

Disks
.....
*Only required if deleted*

Docs: `GCE Disks`_

Create ``3`` SSD disks::

  $ gcloud compute disks create ssd-play{1..3} \
      --project crate-gce \
      --type pd-ssd \
      --zone us-central1-b \
      --size 50GB


Instances
.........

Docs: `GCE Instances`_

**For each unique cluster you will need to update the ``cloud-config.yaml``
with a new discovery token that can be generated with:**

  $  curl -w "\n" 'https://discovery.etcd.io/new?size=3'

Launch ``3`` instances of type ``n1-standard-8`` (``8`` cores, ``30GB`` RAM)
with the given ``cloud-config.yml``::

  $ for i in {1..3}; do gcloud compute instances create play$i \
      --project crate-gce \
      --machine-type n1-standard-8 \
      --image coreos \
      --zone us-central1-b \
      --network play \
      --disk name=ssd-play$i \
      --boot-disk-size 10GB \
      --metadata-from-file user-data=cloud-config.yaml; done


Install Crate
-------------

Upload service file (``crate.service``) to one of the nodes.

Since it is a global service, you can simply run ``fleetctl start``::

  $ fleetctl start crate.service

Update Cluster
--------------

Restarting automatically pulls the latest version from Docker::

  $ fleetctl stop crate.service
  $ fleetctl start crate.service
  
The easiest way to access it directly is over `GCE Web Console`_. 


.. _`Google Cloud SDK`: https://cloud.google.com/sdk/
.. _`GCE Networking`: https://cloud.google.com/compute/docs/networking
.. _`GCE Instances`: https://cloud.google.com/compute/docs/instances
.. _`GCE Disks`: https://cloud.google.com/compute/docs/disks
.. _`GCE Web Console`: https://console.cloud.google.com/compute/instances?project=crate-gce
