#!/bin/sh

#idx=enwiki-latest-pages-meta-history10
idx=$1
url="http://localhost:9200/$idx"

#curl -Ss -XDELETE "$url?pretty"

curl -Ss -XPUT "$url?pretty" -d @wikipedia_hist_mapping.json

#curl -Ss "$url/_settings?pretty"

