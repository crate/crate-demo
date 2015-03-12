# -*- coding: utf-8 -*-

import os
import json
import time
from datetime import datetime

from fabric.api import env, task, run, local, roles, settings
from fabric.operations import put
from fabric.contrib.files import upload_template
from fabric.context_managers import cd, quiet
from fabric.colors import red, green, yellow

LOCUST_DIR = '/home/admin/sandbox/locust'
NODES = [
        ...
]

env.forward_agent = True
env.user = 'admin'
env.roledefs = {
    'node': NODES
    }

CRATE_HOST = '127.0.0.1'
CRATE_PORT = 4200

# Settings for GCE cluster
MASTER_IP = '<MASTER_IP>'
MASTER_HOST = '<MASTER_HOSTNAME>'
SLAVE_HOSTS = [
        ...
]

DIRS = [
    'var/log/supervisor',
]

sv_fname = 'supervisor.conf'
sv_conf = os.path.join(LOCUST_DIR, sv_fname)

def context():
    is_master = run('hostname') == MASTER_HOST
    return dict(
        is_master = is_master,
        master_node = MASTER_IP,
        crate = dict(
            host = CRATE_HOST,
            port = CRATE_PORT,
            ),
        )


@roles('node')
def update_tests():
    with cd(LOCUST_DIR):
        put('loadtest.py', 'loadtest.py')


@roles('node')
def setup():
    with cd(LOCUST_DIR):
        for d in DIRS:
            run('mkdir -pv {0}'.format(d))

        put('loadtest.py', 'loadtest.py')
        upload_template(sv_fname, sv_fname,
                        context=context(), backup=False, use_jinja=True)
        with quiet():
            run('bin/supervisorctl -c {0} stop all'.format(sv_conf))
            run('bin/supervisorctl -c {0} shutdown'.format(sv_conf))
        time.sleep(2)
        run('bin/supervisord -c {0}'.format(sv_conf))


@roles('node')
def shutdown():
    with cd(LOCUST_DIR):
        run('bin/supervisorctl -c {0} stop all'.format(sv_conf))
        run('bin/supervisorctl -c {0} shutdown'.format(sv_conf))


@roles('node')
def start():
    is_master = run('hostname') == MASTER_HOST
    with cd(LOCUST_DIR):
        with quiet():
            run('bin/supervisorctl -c {0} stop all'.format(sv_conf))
        prog = is_master and 'locust-master' or 'locust-slave'
        run('bin/supervisorctl -c {0} start {1}'.format(sv_conf, prog))


@roles('node')
def status():
    hostname = run('hostname')
    is_master = hostname == MASTER_HOST
    with cd(LOCUST_DIR):
        print('[{0}] {1} ({2})'.format(
            yellow(hostname),
            green(env.user + '@' + env.host),
            is_master and green('master') or red('slave'),
            ))
        with settings(warn_only=True):
            run('bin/supervisorctl -c {0} status'.format(sv_conf))
