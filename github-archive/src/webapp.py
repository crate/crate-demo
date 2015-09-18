# -*- coding: utf-8; -*-
# vi: set encoding=utf-8

import os
import sys
import logging

from argparse import ArgumentParser

from tornado.ioloop import IOLoop
from tornado.options import parse_command_line, define, options
from tornado.web import Application


LOGGER = logging.getLogger(__name__)

define('port', default=8000, type=int, help='http port')
define('host', default='127.0.0.1', type=str, help='bind host')


def get_app(root, debug):
    settings = dict(
        debug=debug,
        compress_response=True,
        static_path=os.path.join(root, 'webapp'),
        static_url_prefix='/',
        static_hash_cache=False,
    )
    return Application([], **settings)


def server():
    '''simple webserver that serves static files from webapp/ directory'''
    parse_command_line()

    app = get_app(os.getcwd(), True)
    app.listen(options.port)

    LOGGER.info('Serving webapp at http://{}:{}/index.html'
                .format(options.host, options.port))
    LOGGER.debug('Press Ctrl+C to stop server')
    try:
        IOLoop.current().start()
    except KeyboardInterrupt:
        LOGGER.warn('Stopping ...')
        IOLoop.current().stop()
    finally:
        sys.exit()
