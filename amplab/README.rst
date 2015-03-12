===================
Convert AmpLab Data
===================

The benchmark data consists of 2 tables (``rankings``, ``uservisits``)
each with 3 sets of different sizes (``tiny``, ``1node``, ``5nodes``).

`More info <https://amplab.cs.berkeley.edu/benchmark/>`_.

Create folder structure::

  - tiny
    - rankings
    - rankings_json
    - uservisits
    - uservisits_json
  - 1node
    - rankings
    - rankings_json
    - uservisits
    - uservisits_json
  - 5nodes
    - rankings
    - rankings_json
    - uservisits
    - uservisits_json

Download data from S3::

    $ s3cmd get -r s3://big-data-benchmark/pavlo/text/<size>/<table>/ ./<size>/<table>/

Convert dataset::

    $ python convert_rankings.py -s <size>/rankings/ -t <size>/rankings_json/
    $ python convert_visits.py -s <size>/uservisits/ -t <size>/uservisits_json/

Gzip json files::

    $ gzip <size>/<table>_json/part-*

Upload to S3::

    $ s3cmd put <size>/<table>_json/part-* s3://crate.amplab/data/<size>/<table>/



Converted Datasets on S3
------------------------

All converted files are available on the S3 bucket ``crate.amplab``.

tiny::

    s3://crate.amplab/data/tiny/rankings/
    s3://crate.amplab/data/tiny/uservisits/

1node::

    s3://crate.amplab/data/1node/rankings/
    s3://crate.amplab/data/1node/uservisits/

5nodes::

    s3://crate.amplab/data/5nodes/rankings/
    s3://crate.amplab/data/5nodes/uservisits/


Import from S3
--------------

Create tables::

    queries/rankings.sql

    queries/uservisits.sql

uservisits tiny::

    ./queries/import_uservisits_tiny.sql

uservisits 1node::

    ./queries/import_uservisits_1node.sql

uservisits 5nodes::

    queries/import_uservisits_5nodes.sql

rankings tiny::

    ./queries/import_rankings_1node.sql

rankings 1node::

    ./queries/import_rankings_1node.sql

rankings 5nodes::

    ./queries/import_rankings_5nodes.sql


Record count:

+---------+--------------+-----------------------+-----------------------+--------------------------------------------+
| Dataset | Scale Factor | Rankings (documented) | Rankings (actual st1) | Rankings (actual Crate - unique due to PK) |
+=========+==============+=======================+=======================+============================================+
| /tiny/  | small        | 1.200                 | 1.200                 | 1.200                                      |
+---------+--------------+-----------------------+-----------------------+--------------------------------------------+
| /1node/ | 1            | 18 Million            | 17.999.999            | 17.929.294                                 |
+---------+--------------+-----------------------+-----------------------+--------------------------------------------+
| /5nodes | 5            | 90 Million            | 90.000.000            | 90.000.000                                 |
+---------+--------------+-----------------------+-----------------------+--------------------------------------------+


+---------+--------------+-------------------------+-------------------------+----------------------------------------------+
| Dataset | Scale Factor | UserVisits (documented) | UserVisits (actual st1) | UserVisits (actual Crate - unique due to PK) |
+=========+==============+=========================+=========================+==============================================+
| /tiny/  | small        | 10.000                  | 10.000                  | 10.000                                       |
+---------+--------------+-------------------------+-------------------------+----------------------------------------------+
| /1node/ | 1            | 155 Million             | 154.999.997             | 153.956.289                                  |
+---------+--------------+-------------------------+-------------------------+----------------------------------------------+
| /5nodes | 5            | 775 Million             | 751.754.869             | 751.754.869                                  |
+---------+--------------+-------------------------+-------------------------+----------------------------------------------+

