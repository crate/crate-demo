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
