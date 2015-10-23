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


def delta_month(date, months):
    return date + timedelta(months * 365 / 12)

def create_table(cur, schema_file):
    with open (schema_file, "r") as schema:
        try:
            cur.execute(schema.read())
        except Exception as e:
            print("error on table creation\n {}".format(e))

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--start', help='start date', required=True)
    parser.add_argument('-e','--end', help='end date', required=True)
    parser.add_argument('-H','--host', help='host', required=True)
    return parser.parse_args()

def alter_table(cur, number_of_replicas):
    try:
        cur.execute("""ALTER TABLE github SET (number_of_replicas=?)""", (number_of_replicas,))
        print("alter table to number_of_replicas={}".format(str(number_of_replicas)))
    except Exception as e:
        print("error on alter table \n {}".format(e))

def main():
    try:
        aws_secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
        aws_access_key = os.environ['AWS_ACCESS_KEY_ID']
    except KeyError:
        print("Please set your AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID environment variables.")
        return 1

    args = parse_args()

    start_date = datetime.strptime(args.start, "%Y/%m")
    end_date = datetime.strptime(args.end, "%Y/%m")

    connection = client.connect(args.host, error_trace=True)
    cur = connection.cursor()

    create_table(cur, os.path.join(os.path.dirname(__file__), "..", "schema.sql"))
    alter_table(cur, 0)

    diff = end_date - start_date
    all_days = [end_date - timedelta(days=d) for d in range(diff.days)]
    for month in set([datetime.strftime(day, '%Y-%m') for day in all_days]):
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
    sys.exit(main())

