#!/usr/bin/env python

from __future__ import print_function

import sys
import time
import json

from argparse import ArgumentParser
from crate.client import connect

from fabric.api import run, task, abort, env, hosts
from fabric.colors import green, red
from fabric.operations import put
from fabric.main import parse_arguments
from fabric.contrib import files
from fabric.context_managers import cd
from fabric import state


def timestamp():
    return int(time.time() * 1000)


def get_value_from_dict(dic, path):
    for k in path.split('.'):
        dic = dic.get(k)
    return dic


class MetricFetcher(object):

    def __init__(self, hosts):
        """
        initialize a new MetricFetcher

        :param hosts: list of crate hosts to connect to
        """

        conn = connect(hosts)
        self.cursor = conn.cursor()
        self.metrics = {}

    def cleanup_metrics(self):
        self.metrics = {t: metrics for t, metrics in self.metrics.iteritems() if t >= timestamp() - 5000}

    def metrics_for_node(self, name):
        metrics = {}
        for t, rows in self.metrics.iteritems():
            for row in rows:
                if row['name'] == name:
                    metrics[t] = row
        return metrics

    def avg_metric_per_s(self, node_name, key):
        metric = {}
        for t, rows in self.metrics_for_node(node_name).iteritems():
            metric[t] = get_value_from_dict(rows, key)
        min_t = min(metric.keys())
        max_t = max(metric.keys())
        if max_t - min_t == 0:
            return 0.0
        return 1000.0 * (metric[max_t] - metric[min_t]) / float((max_t - min_t))

    def _row_to_dict(self, row):
        d = dict()
        cols = ['name', 'load', 'cpu_used', 'heap_used', 'transactions', 'packets']
        for i in range(len(cols)):
            d[cols[i]] = row[i]
        return d

    def _generate_result(self, rows):
        rows = [self._row_to_dict(row) for row in rows]
        ts = timestamp()
        self.metrics[ts] = rows
        self.cleanup_metrics()
        for row in rows:
            name = row['name']
            row['transactions_per_second'] = self.avg_metric_per_s(name, 'transactions')
            row['packets_per_second'] = self.avg_metric_per_s(name, 'packets')
        return {
            'timestamp': ts,
            'rows': rows
        }

    def fetch(self):
        """
        fetches the current load from the crate nodes

        result is returned as python dict in the following format:

            {
                'timestamp': <timestamp>
                'rows': [
                    {
                        'name': <node_name>,
                        ...
                    }
                ]
            }

        """
        self.cursor.execute('''select name,
        load['1'] as load,
        os['cpu']['used'] as cpu_used,
        heap['used']*100.0/heap['max'] as heap_used,
        fs['total']['reads']+fs['total']['writes'] as total_transactions,
        network['tcp']['packets']['sent']+network['tcp']['packets']['received'] as total_packets
        from sys.nodes''')
        rows = self.cursor.fetchall()
        return self._generate_result(rows)

@task
def metrics():
    fetcher = MetricFetcher(env.hosts)
    while True:
        print(json.dumps(fetcher.fetch(), separators=(',',':')))
        time.sleep(1)
