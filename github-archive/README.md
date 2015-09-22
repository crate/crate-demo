# Github Archive on AWS
This document describes how a Crate cluster can be setup to present how Crate
analyses [Github Archive Data](https://www.githubarchive.org/).

## Bootstrapping
Run buildout in your shell to get the [aws cli](https://aws.amazon.com/cli/):

```sh
python bootstrap.py
bin/buildout
```

### Providing your AWS credentials
Set the following environment variables with your credentials.

```sh
export AWS_ACCESS_KEY_ID='...'
export AWS_SECRET_ACCESS_KEY='...'
```

## Run the cluster
Once the set up is finished the cluster is ready to start. This can be done by 
running ``start-cluster.sh`` over the **CLI** or by using the **AWS Management 
Console**.

### Using the CLI
Further define them in the AWS CLI configuration by using the command:
```sh
bin/aws configure
```
Set Default region name to ``us-west-2`` and leave the default output format at
 ``JSON``.

Run the following command to display the available parameters.
```sh
./start-cluster.sh help
```

If you want to start a 16-node-cluster in ``us-west-2`` with the key-name 
``github-archive`` this command will be like follows:

```sh
./start-cluster.sh 16 github-archive
```

### Using AWS Management Console
Insert your AWS credentials ``__AWS_ACCESS_KEY_ID__`` and 
``__AWS_SECRET_ACCESS_KEY__`` into the existing ``user-data.sh`` in the 
appropriate fields. 


## Data queries


## Visualization of the data via the WebApp
The web application provides queries and a corresponding visualization of the
data provided with Crate. Requires ```npm``` to work.

```sh
cd webapp
npm install
npm start
```

## Importing data
Import data from s3 to the Crate cluster:

```sh
bin/imp --start 2011/8 --end 2011/10 --host localhost:4200
```
