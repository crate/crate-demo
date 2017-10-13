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


import argh
from eden.collector import StatsCollector
from eden.picameracapture import PiCameraCapture
from eden.auth import get_token
from eden.server import run_server
import toml
import asyncio
import logging
from threading import Thread


def capture(config_file_name='config.toml'):
    'Capture and analyze camera input and store the results on a server.'

    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s %(levelname)s:%(name)s %(message)s')
    logging.info('Starting eden picam')

    with open(config_file_name) as conffile:
        config = toml.loads(conffile.read())
    logging.info('Parsed config')

    eden_server_conf = config["eden-server"]
    agent_conf = config["agent"]
    mjpeg_server_conf = config["mjpeg-server"]

    token = get_token(eden_server_conf["secret"], agent_conf[
                      "name"], agent_conf["role"])

    loop = asyncio.get_event_loop()

    logging.info('Creating collector')
    collector = StatsCollector(loop=loop, token=token, batch_size=eden_server_conf[
        "batch_size"], endpoint=eden_server_conf["endpoint"])

    camcap = PiCameraCapture(**config["camera"])

    if mjpeg_server_conf["enable"]:
        logging.info('Starting MJPEG server')
        mjpeg_server = Thread(target=lambda: run_server(camcap, mjpeg_server_conf[
                              "host"], mjpeg_server_conf["port"]), daemon=True)
        mjpeg_server.start()

    logging.info('Starting detector')
    t = Thread(target=lambda: camcap.detect(
        collector, **config["haarcascades"]), daemon=True)
    t.start()

    logging.info('Starting event loop')
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info("Shutting down...")
    finally:
        camcap.stop()
        t.join()


def main():
    argh.dispatch_command(capture)

if __name__ == '__main__':
    main()
