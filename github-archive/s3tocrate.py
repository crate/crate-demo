#!/usr/bin/python

import argparse
import os
import sys
from datetime import date, timedelta, datetime
from crate import client
from urllib import quote_plus

def delta_month(date, months):
    return date + timedelta(months*365/12)

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-s','--start', help='start date', required=True)
  parser.add_argument('-e','--end', help='end date', required=True)
  parser.add_argument('-host','--host', help='host', required=True)
  return parser.parse_args()

def main():
  aws_secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
  aws_access_key = os.environ['AWS_ACCESS_KEY_ID']

  args = parse_args()

  start_date = datetime.strptime(args.start, "%Y/%m")
  end_date = datetime.strptime(args.end, "%Y/%m")

  connection = client.connect(args.host)
  cur = connection.cursor()

  for single_date in (start_date + timedelta(n) for n in range((delta_month(end_date, 1) - start_date).days)):
    import_data = single_date.strftime("%Y-%m-%d");
    month_partition = single_date.strftime("%Y-%m");

    print('Importing github data for {0} ...'.format(import_data))
    s3_url = 's3://{0}:{1}:@crate.sampledata/github/{2}-*'.format(quote_plus(aws_access_key),
      quote_plus(aws_secret_key), import_data)
    cur.execute("""COPY github PARTITION (month_partition=?)
      FROM ? WITH (bulk_size=1000, compression='gzip')""",
      (month_partition, s3_url))

if __name__=='__main__':
  main()