# Copyright 2017 Crate.IO GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import asyncio
import logging


class StatsCollector:

    def __init__(self, token, endpoint, batch_size, loop):
        self.endpoint = endpoint
        self.headers = {"Content-Type": "application/json; charset=utf-8",
                        "Authorization": "Bearer %s" % token}
        self.batch_size = batch_size
        self.batch = []
        self.loop = loop

    async def append_send(self, data):
        ts = data[0]
        readings = data[1]
        meta = data[2]
        stats = {"timestamp": ts, "data": readings, "meta": {"name": meta}}
        self.batch.append(stats)
        logging.debug('Appending %s', stats)

        if len(self.batch) >= self.batch_size:
            data = json.dumps(self.batch).encode("utf8")
            l = len(data)
            self.headers.update({"Content-Length": l})
            req = Request(self.endpoint, data=data, headers=self.headers)
            logging.debug("Sending: %s", data)
            try:
                logging.info("Sending %d items", len(self.batch))
                response = urlopen(req)
                self.batch = []
                logging.info('Sent!')
            except Exception as e:
                logging.error('Server responded with an error code: %s' % e)


    def collect(self, stats):
        self.loop.call_soon_threadsafe(
            asyncio.ensure_future, self.append_send(stats))
