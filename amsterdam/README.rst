============================
A Simple Locust Query Tester
============================

Prepare python
==============

It's best to create a virtual environment and then install::

    $ pip install crate
    $ pip install locustio

In case you can't install locust on your OSX machine, try this::

    $ export CFLAGS=-Qunused-arguments
    $ export CPPFLAGS=-Qunused-arguments

Create Test Database
====================

Create initial database table::

    $ python createdata.py localhost:4200 1000000


Locust Test Runner
==================

Run locust::

    $ python run.py -f loadtest/query.py --host="crate1:4200 crate2:4200"

Now the locust frontend is available at localhost:8089


Add New Queries
===============

See loadtest/query.py on how to extend the queries.
