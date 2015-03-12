#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import sys
import datetime
import time
import argparse
from multiprocessing import Process, JoinableQueue

DEFAULT_SOURCE_FOLDER = './uservisits'
DEFAULT_TARGET_FOLDER = './uservisits_json'
DEFAULT_CONCURRENCY = 10


def convert(source_folder, target_folder, concurrency):
    q = JoinableQueue(concurrency * 2)
    uservisits_files = os.listdir(source_folder)

    target_folder_exists(target_folder, create=True)

    for _ in range(concurrency):
        p = Process(target=do_work, args=(source_folder, target_folder, q,))
        p.daemon = True
        p.start()

    try:
        for fi in uservisits_files:
            q.put(fi)
        q.join()
    except KeyboardInterrupt:
        sys.exit(1)


def target_folder_exists(target_folder, create=True):
    if not os.path.exists(target_folder):
        if create:
            os.makedirs(target_folder)
            return True
        return False


def do_work(source_folder, target_folder, q):
    while True:
        filename = q.get()
        print("Convert {0} ...".format(filename))
        with open(os.path.join(target_folder, filename), 'w') as output:
            for line in open(os.path.join(source_folder, filename)):
                output.write(convert_line(line))
        q.task_done()


def convert_line(line):
    parts = line.rstrip().split(',')
    if len(parts) < 9:
        new_parts = [''] * 9
        for i in range(9):
            try:
                new_parts = parts[i]
            except IndexError:
                break
        parts = new_parts
    visitDate = parts[2]
    visitDate = datetime.datetime.strptime(visitDate, '%Y-%m-%d')
    visitDate = int(1000 * time.mktime(visitDate.timetuple()))
    data = {
        'sourceIP': parts[0],
        'destinationURL': parts[1],
        'visitDate': visitDate,
        'adRevenue': parts[3],
        'UserAgent': parts[4],
        'cCode': parts[5],
        'lCode': parts[6],
        'searchWord': parts[7],
        'duration': parts[8]
    }
    return json.dumps(data) + '\n'


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Convert 'user visits' CSV to JSON.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-s',
        '--source-folder',
        default=DEFAULT_SOURCE_FOLDER,
        help="source folder of CSVs with 'user visits'."
    )
    parser.add_argument(
        '-t',
        '--target-folder',
        default=DEFAULT_TARGET_FOLDER,
        required=False,
        help='target folder to which the JSON files will get generated to.'
    )
    parser.add_argument(
        '-c',
        '--concurrency',
        type=int,
        default=DEFAULT_CONCURRENCY,
        required=False,
        help='process with x processes (where x = CONCURRENCY)'
    )
    args = parser.parse_args()
    convert(args.source_folder, args.target_folder, args.concurrency)

