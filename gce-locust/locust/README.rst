================
Locust Load Test
================

Setup with bootstrap::

    $ python2.7 bootstrap.py
    $ ./bin/buildout

Setup with virtualenv::

    $ virtualenv -p python2.7 .
    $ pip install -r requirements.txt


Local Locust
------------

    $ bin/locust -f loadtest.py --host 127.0.0.1:4200

Distributed Locust
------------------

In order to run locust distributed you need to configure the setup in
the ``fabfile.py``.

The settings are::

    CRATE_HOST
    CRATE_PORT
    MASTER_IP
    MASTER_HOST
    SLAVE_HOSTS

Then run the ``setup`` task to configure and start ``supervisord``
on all nodes::

    $ bin/fab setup

To start locust on all nodes::

    $ bin/fab start

To check the status run::

    $ bin/fab status


Connect to the master node and forward the locust port::

    ssh -L 8089:localhost:8089 admin@X.X.X.X

Open browser to start tests::

    http://localhost:8089

