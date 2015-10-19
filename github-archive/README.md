# Github Archive on AWS

This document describes how a Crate cluster can be setup to present how Crate
analyses [Github Archive Data](https://www.githubarchive.org/).

## Bootstrapping

Run buildout in your shell to get the [aws cli](https://aws.amazon.com/cli/):

```console
$ python3.4 bootstrap.py
$ bin/buildout -N
```

### Providing your AWS credentials

Set the following environment variables with your credentials.

```console
$ export AWS_ACCESS_KEY_ID='...'
$ export AWS_SECRET_ACCESS_KEY='...'
```

## Run the cluster

Once the set up is finished the cluster is ready to start. This can be done by
running ``start-cluster.sh`` over the **CLI** or by using the **AWS Management
Console**.

### Using the CLI

Further define them in the AWS CLI configuration by using the command:

```console
$ bin/aws configure
```

Set Default region name to ``us-west-2`` and leave the default output format at
 ``JSON``.

Run the following command to display the available parameters.

```console
$ ./launch.sh help
```

If you want to start a 16-node-cluster using AMI in ``us-west-2`` with the key-name
``github-archive`` this command will be like follows:

```console
$ ./launch.sh 16 github-archive ami-c1b9a0f1
```

### Using AWS Management Console

Insert your AWS credentials ``__AWS_ACCESS_KEY_ID__`` and
``__AWS_SECRET_ACCESS_KEY__`` into the existing ``user-data.sh`` in the
appropriate fields.

## Data queries


## Visualization of the data via the WebApp

The web application provides queries and a corresponding visualization of the
data provided with Crate.

```console
$ bin/bower install
$ bin/webapp [--port=PORT | --host=HOST | --logging=LOGLEVEL | --help]
```

Forward port `4200` to `localhost`:

Get a list of nodes public DNS names and use one of them in the port forwarding.

```console
bin/aws ec2 describe-instances --filters Name=tag:Name,Values=Crate-Github-Data Name=instance-state-name,Values=running
```

```console
$ ssh -i ~/.ssh/github-archive.pem -L 4200:localhost:4200 ec2-user@public_dns_name
```

## Github Data table
The SQL query for creation of the github data table can be found in the
``schema.sql`` file. If the port forwarding command from the previous section was apllied
connect to the crate cluster via ``crash`` or ``Admin UI`` on ``localhost:4200`` and create the table
using the given query.

## Importing data
Import data from s3 to the Crate cluster:

```console
$ bin/import --start 2011/8 --end 2011/10 --host localhost:4200
```

## Importing github data to S3
Import data from github archive to S3 buckets:

Run the script with ``start`` and ``end`` arguments to import the range of files.

```console
$ bin/copy_github_data --prefix small_github --bucket crate.sampledata --start 2015-09-30-01 --end 2015-09-30-19
```

Run the script with ``shift`` argument to import the github archive file
generated ``N`` of hours ago.

```console
$ bin/copy_github_data --prefix small_github --bucket crate.sampledata --shift -4
```
