#!/usr/bin/python

import os
import sys
import argparse
try:
    from urllib.parse import quote_plus
except ImportError:
    # python 2.x fallback
    from urllib import quote_plus
from datetime import date, timedelta, datetime
from crate import client

def make_ts(date_string):
    return datetime.strptime(date_string, "%Y/%m")

def create_table(cur, schema_file):
    with open (schema_file, "r") as schema:
        try:
            cur.execute(schema.read())
        except Exception as e:
            print("error on table creation\n {}".format(e))

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--start', help='start date', type=make_ts, required=True)
    parser.add_argument('-e','--end', help='end date', type=make_ts, required=True)
    parser.add_argument('-H','--host', help='host', required=True)
    return parser.parse_args()

def alter_table(cur, number_of_replicas):
    try:
        cur.execute("""ALTER TABLE github SET (number_of_replicas=?)""", (number_of_replicas,))
        print("alter table to number_of_replicas={}".format(str(number_of_replicas)))
    except Exception as e:
        print("error on alter table \n {}".format(e))

def get_month_partitions(start_date, end_date):
    """
    >>> start = make_ts('2015/1')
    >>> end = make_ts('2015/6')
    >>> get_month_partitions(start, end)
    ['2015-01', '2015-02', '2015-03', '2015-04', '2015-05', '2015-06']

    >>> start = make_ts('2015/1')
    >>> end = make_ts('2015/1')
    >>> get_month_partitions(start, end)
    ['2015-01']

    >>> start = make_ts('2014/12')
    >>> end = make_ts('2015/2')
    >>> get_month_partitions(start, end)
    ['2014-12', '2015-01', '2015-02']

    >>> start = make_ts('2015/12')
    >>> end = make_ts('2015/10')
    >>> get_month_partitions(start, end)
    End date must not be less than start date.
    []
    """
    if end_date < start_date:
        print("End date must not be less than start date.")
        return []

    diff = (end_date - start_date) + timedelta(days=1)
    all_days = [start_date + timedelta(days=d) for d in range(diff.days)]
    months = list(set([datetime.strftime(day, '%Y-%m') for day in all_days]))
    months.sort()
    return months

def main():
    try:
        aws_secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
        aws_access_key = os.environ['AWS_ACCESS_KEY_ID']
    except KeyError:
        print("Please set your AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID environment variables.")
        return 1

    args = parse_args()

    connection = client.connect(args.host, error_trace=True)
    cur = connection.cursor()

    create_table(cur, os.path.join(os.path.dirname(__file__), "..", "schema.sql"))
    alter_table(cur, 0)

    for month in get_month_partitions(args.start, args.end):
        print('Importing Github data for {0} ...'.format(month))
        s3_url = 's3://{0}:{1}@crate.sampledata/github_archive/{2}-*'.format(quote_plus(aws_access_key),
            quote_plus(aws_secret_key), month)
        print('>>> {0}'.format(s3_url))
        cmd = '''COPY github PARTITION (month_partition=?) FROM ? WITH (compression='gzip')'''
        try:
            cur.execute(cmd, (month, s3_url,))
        except Exception as e:
            print("Error while importing {}: {}".format(s3_url, e))
            print(e.error_trace)

    alter_table(cur, 1)
    return 0

if __name__=='__main__':
    import doctest
    doctest.testmod()

