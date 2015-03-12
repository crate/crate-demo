============================================
Amplab Benchmark on Softlayer Infrastructure
============================================

Softlayer
=========

Hardware Configuration
----------------------

The `benchmark <https://amplab.cs.berkeley.edu/benchmark/#hardware>`_
is run on a cluster of `Amazon m2.4xlarge <http://www.ec2instances.info/>`_
instances. The equivalent on Softlayer is the following configuration:

- 1/5 virtual servers
- 8x 2.0GHz cores
- 64 GB memory
- 1 Gbps public/private network interface
- >=100 GB local storage

Salt Configuration
------------------

`crate/salt <https://github.com/crate/salt>`_

example ``/etc/salt/cloud.profiles``::

  softlayer:
    provider: crate-softlayer
    domain: crate.io
    image: CENTOS_6_64
    location: ams01
    cpu_number: 8
    ram: 65536 # 64G
    disk_size: 100 #G
    local_disk: True
    max_net_speed: 1000
    hourly_billing: False
    private_vlan: 477758 (id of your vlan on Softlayer)
    minion:
      grains:
        role:
          - crate_softlayer

example ``/etc/salt/cloud.map``::

  softlayer:
    - sl1
    - sl2
    - sl3
    - sl4
    - sl5

start instances::

    salt-cloud -m /etc/salt/cloud.map -P

provisioning::

    salt -G 'role:crate_softlayer' state.highstate


Install and run Crate
=====================

`pypsh <https://warehouse.python.org/project/pypsh/>`_ is a
simple commandline tool to execute a command in parallel
on multiple hosts.::

    pip install pypsh

Get the IPs of the instances via the Softlayer CLI.
First install the Softlayer Python bindings::

    pip install SoftLayer

and provide your username and API key::

    sl vs config setup

Then you're able to list your instances::

    sl vs list

.. note::

    To make access to the instances easier you should add the IPs
    to your ``/etc/hosts`` file!

Example::

    pypsh 'sl.*\.fir\.io' "/home/admin/crate/upgrade_nightly.py crate-0.40.0-201407092202-95ace36.tar.gz"
    pypsh 'sl.*\.fir\.io' "export AWS_ACCESS_KEY_ID='abc'; export AWS_SECRET_KEY='xyz'; /home/admin/crate/crate_dev_init.sh start"


.. note::

    Crate will be running on its default port but on port ``44200``.


Import Data
===========

The converted data is hosted on a public S3 bucket.

rankings::

    s3://crate.amplab/data/tiny/rankings/
    s3://crate.amplab/data/1node/rankings/
    s3://crate.amplab/data/5nodes/rankings/

uservisits::

    s3://crate.amplab/data/tiny/uservisits/
    s3://crate.amplab/data/1node/uservisits/
    s3://crate.amplab/data/5nodes/uservisits/

SQL statements for the import are provided
with salt provisioning.

.. note::

    The import scripts are executed on a single node
    of the cluster. (Given hostnames are only examples.)

tiny::

    [tiny] /home/admin/sandbox/crash --hosts 127.0.0.1:44200 < /home/admin/sandbox/import_tiny.sql

    [tiny]: COPY OK, 1200 rows affected (2.248 sec)
    [tiny]: COPY OK, 10000 rows affected (3.418 sec)

1node::

    [1node] /home/admin/sandbox/crash --hosts 127.0.0.1:44200 < /home/admin/sandbox/import_1node.sql

    [1node]: COPY OK, 17999999 rows affected (870.955 sec)
    [1node]: COPY OK, 154999997 rows affected (12750.589 sec)

5nodes::

    [5node1] /home/admin/sandbox/crash --hosts 127.0.0.1:44200 < /home/admin/sandbox/import_5nodes.sql


Run Benchmark
=============

repo: `crate/benchmark <https://github.com/crate/benchmark>`_

Start the benchmark runnert from your local maschine::

    ./bin/run-query --crate --crate-hosts <host1> [<host2>, ...] -q {1,2}{a,b,c}


Fetch Metrics
=============

Run buildout::

    cd softlayer
    python2.7 bootstrap.py
    bin/buildout -N

Sample metrics::

    bin/capture metrics --host <host:port> > metrics.json

External Docs
=============

- `salt.cloud.clouds.softlayer <http://docs.saltstack.com/en/latest/ref/clouds/all/salt.cloud.clouds.softlayer.html>`_
- `SoftLayer Python CLI <https://softlayer-python.readthedocs.org/en/latest/cli.html>`_

