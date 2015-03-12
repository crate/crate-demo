#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import sys
import argparse
from multiprocessing import Process, JoinableQueue

DEFAULT_SOURCE_FOLDER = './rankings'
DEFAULT_TARGET_FOLDER = './rankings_json'
DEFAULT_CONCURRENCY = 10


def convert(source_folder, target_folder, concurrency):
    q = JoinableQueue(concurrency * 2)
    rankings_files = os.listdir(source_folder)

    target_folder_exists(target_folder, create=True)

    for _ in range(concurrency):
        p = Process(target=do_work, args=(source_folder, target_folder, q,))
        p.daemon = True
        p.start()

    try:
        for fi in rankings_files:
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
    if len(parts) < 3:
        new_parts = [''] * 3
        for i in range(3):
            try:
                new_parts = parts[i]
            except IndexError:
                break
        parts = new_parts
    data = {
        'pageURL': parts[0],
        'pageRank': parts[1],
        'avgDuration': parts[2]
    }
    return json.dumps(data) + '\n'


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Converts 'rankings' CSV to JSON.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-s',
        '--source-folder',
        default=DEFAULT_SOURCE_FOLDER,
        help='source folder of CSVs with rankings'
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

