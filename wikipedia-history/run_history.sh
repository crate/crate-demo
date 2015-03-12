#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PY=/opt/python-2.7/bin/python
D_IN=/mnt/data20/wikipedia_history
D_OUT=/mnt/data21/wikipedia_history/json

#find /mnt/data20/wikipedia_history/ -name '*.bz2'|sort|head -n 1



NAME=$1
F=$D_IN/$NAME

#enwiki-latest-pages-meta-history10.xml-p000925001p000972034.bz2

if [ -f $F ];
then
   echo "Processing $F"
else
   echo "File $F not found"
   exit 1
fi

F=$D_IN/$NAME

if [ -e $D_OUT/$NAME ];
then
   echo "Folder exists:" $D_OUT/$NAME/
   exit 1
else
   echo "out:" $D_OUT/$NAME/
fi

mkdir -p $D_OUT/$NAME || exit 1

echo $(date) > $D_OUT/$NAME/started || exit 1

bunzip2 < $D_IN/$NAME |$PY $DIR/history.py | split -l 100000 -a 4 - $D_OUT/$NAME/json.

echo $(date) > $D_OUT/$NAME/ended

ls -alh $D_OUT/$NAME/


