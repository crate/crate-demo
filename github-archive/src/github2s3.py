#!/usr/bin/python

import os
import sys
import boto
import argparse
import ssl
import requests
from urllib.request import urlretrieve
from boto.s3.key import Key
from boto.s3.connection import S3Connection
from datetime import datetime, timedelta

MAX_RETRIES = 3

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

if AWS_ACCESS_KEY_ID is None or AWS_SECRET_ACCESS_KEY is None:
    print('AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY is not set')
    sys.exit()

_old_match_hostname = ssl.match_hostname

def _new_match_hostname(cert, hostname):
    if hostname.endswith('.s3.amazonaws.com'):
        pos = hostname.find('.s3.amazonaws.com')
        hostname = hostname[:pos].replace('.', '') + hostname[pos:]
    return _old_match_hostname(cert, hostname)

ssl.match_hostname = _new_match_hostname

def upload_to_s3(file_name, bucket, key, content_type=None):
    if os.path.exists(file_name):
        with open(file_name, mode='r+') as fp:
            try:
                size = os.fstat(fp.fileno()).st_size
            except:
                fp.seek(0, os.SEEK_END)
                size = fp.tell()

            k = Key(bucket)
            k.key = key
            if content_type:
                k.set_metadata('Content-Type', content_type)
            sent = k.set_contents_from_filename(file_name, cb=None, md5=None, reduced_redundancy=False)

            fp.seek(0)
            return sent == size
    else:
        return False

def exists_url(path):
    r = requests.head(path)
    return r.status_code == requests.codes.ok

def generate_key_name(diff):
    key_time = datetime.now() + timedelta(hours=diff)
    return key_time.strftime("%Y-%m-%d-%-H")

def mkdate(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d-%H")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b','--bucket', help='s3 bucket', required=True)
    parser.add_argument('-p','--prefix', help='s3 bucket prefix', required=True)
    parser.add_argument('-s','--start', help='start date', default=None, type=mkdate, required=False)
    parser.add_argument('-e','--end', help='end date', default=None, type=mkdate, required=False)
    parser.add_argument('-tsh','--shift', help='Shift in hours', type=int, default=0, required=False)

    return parser.parse_args()

def run(bucket_name, prefix_name, key_name):
    s3_key_name = '{}/{}'.format(prefix_name, key_name)
    git_key_url = 'http://data.githubarchive.org/{}'.format(key_name)
    print('Processing {} to s3...'.format(s3_key_name))

    s3_conn = S3Connection()
    bucket = s3_conn.get_bucket(bucket_name)
    key = bucket.get_key(s3_key_name)

    if key:
        print('{} is already in the bucket'.format(key))
    elif exists_url(git_key_url) is False:
        print('{} does not exist'.format(git_key_url))
    else:
        urlretrieve(git_key_url, key_name)

        # pre-process data

        retry_count = 0
        while not upload_to_s3(key_name, bucket, s3_key_name) and retry_count <= MAX_RETRIES:
            retry_count += 1
            print('Failed to upload {} !'.format(s3_key_name))
        else:
            print('File {} is uploaded to {}/{}!'.format(key_name, bucket_name, prefix_name))
        os.remove(key_name)

def main():
    args = parse_args()
    prefix = args.prefix
    bucket = args.bucket
    start_date = args.start
    end_date = args.end

    if start_date and end_date:
        hours = (end_date - args.start).seconds // 60
        keys = [start_date + timedelta(hours=x) for x in range(0, hours + 1)]
        for key_name in keys:
            key = '{}.json.gz'.format(key_name.strftime("%Y-%m-%d-%-H"))
            run(bucket, prefix, key)
    elif args.shift:
        key = '{}.json.gz'.format(generate_key_name(args.shift))
        run(bucket, prefix, key)
    else:
        print('Provided arguments are not correct')

if __name__=='__main__':
    main()

