# -*- coding: utf-8 -*-
# vim: set fileencodings=utf-8

__docformat__ = "reStructuredText"


import sys
import time
import math
import random
import json
import time
import calendar
import argparse
from datetime import date, datetime, timedelta

from faker import Factory
fake = Factory.create()

from crate import client

def create_sampledata(hosts, num_users):
    connection = client.connect(hosts)
    cursor = connection.cursor()

    today = date.today()
    file_count = 1

    for user_id in xrange(num_users):
        profile = fake.profile(['username','name','birthdate','address'])
        date_parts = profile['birthdate'].split('-')

        user = dict(
            username = profile['username'],
            name = profile['name'],
            address = profile['address'],
            )

        dt = datetime(*[int(x) for x in date_parts])
        user['date_of_birth'] = calendar.timegm(dt.utctimetuple())

        days_online = random.randint(0, 365)
        date_joined = datetime.combine(today - timedelta(days=days_online), datetime.min.time())
        user['date_joined'] = int(calendar.timegm(date_joined.utctimetuple()) * 1000)
        user['month_partition'] = date_joined.strftime('%Y%m')

        cursor.execute("""INSERT INTO users (username, name, address, date_of_birth, date_joined, month_partition) VALUES (?, ?, ?, ?, ?, ?)""",
                       [user['username'], user['name'], user['address'],
                        user['date_of_birth'], user['date_joined'],
                        user['month_partition']])

        args = []
        for x in xrange(days_online * 24 * 60):
            y = date_joined + timedelta(minutes=x)
            args.append([
                user['username'],
                int(calendar.timegm(y.timetuple())*1000),
                random.randint(0, 16),
                y.strftime('%Y%m'),
                ])
            if len(args) == 100:
                # batch insert 100 args
                cursor.executemany("""INSERT INTO steps (username, ts, num_steps, month_partition) VALUES (?, ?, ?, ?)""", args)
                args = []
        # insert rest of args
        cursor.executemany("""INSERT INTO steps (username, ts, num_steps, month_partition) VALUES (?, ?, ?, ?)""", args)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('hosts', type=str,
                   help='hosts running Crate')
    parser.add_argument('users', type=int,
                   help='number of users to generate sampledata for')
    args = parser.parse_args()
    print('Inserting sampledata ...')
    create_sampledata(args.hosts.split(','), args.users)
