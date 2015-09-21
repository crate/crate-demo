# Github Archive on AWS
This document describes how a Crate cluster can be setup to present how Crate
analyses [Github Archive Data](https://www.githubarchive.org/).

## Bootstrapping
Run buildout in your shell to get the [aws cli](https://aws.amazon.com/cli/):

```sh
python bootstrap.py
bin/buildout
```

Configure your AWS credentials:

```sh
bin/aws credentials
```

Set Default region name to ``us-west-2`` and leave the default output format at
``None``.

# Querying & visualization of the data via the WebApp
The web application provides queries and a corresponding visualization of the
data provided with Crate. Requires ```npm``` to work.

```cd webapp
npm install
npm start
´´´

# Prepare AWS Credentials for importing data

Provide credentials:

```sh
  export AWS_ACCESS_KEY_ID='...'
  export AWS_SECRET_ACCESS_KEY='...'
```

Import data from s3 to the Crate cluster:

```sh
bin/imp --start 2011/8 --end 2011/10 --host localhost:4200
```