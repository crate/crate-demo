#!/bin/bash

# retrieves the logs from the server

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


for host in $(cut -d ' ' -f 1 $DIR/hostfiles.txt |sort|uniq)
do
    rsync -v $host:sandbox/crate-wikipedia/import.log logs/${host}.import.log
done
