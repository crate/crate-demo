#!/bin/sh

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PY=/opt/python-2.7/bin/python
D_IN=/mnt/data20/wikipedia_history
D_OUT=/mnt/data21/wikipedia_history/json

for d in $(ls -1 $D_OUT |sort)
do
    idx=$(echo $d | cut -d '.' -f 1)
    path=$D_OUT/$d/
    echo $idx
    echo $path
    body='{"directory":"'$path'"}'
    url='http://localhost:9200/'$idx'/default/_import?pretty'
    echo $url
    curl -XPOST $url -d $body || exit 1
done

