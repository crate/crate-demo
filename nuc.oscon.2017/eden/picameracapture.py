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

from picamera import PiCamera
import time
import cv2
import numpy as np
from datetime import datetime
import logging

CHANNELS = 3


class PiCameraCapture:

    def __init__(self, framerate, width, height, mark_faces, *args, **kwargs):
        self.framerate = framerate
        self.width = width
        self.height = height
        self.classifier = cv2.CascadeClassifier(
            '/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')
        self.last_frame = None
        self._stop = False
        self.mark_faces = mark_faces

    def stop(self):
        self._stop = True

    def detect(self, collector, scale_factor, min_neighbors, min_size):
        logging.info('Starting detection')
        frames = 0
        start = int(datetime.utcnow().timestamp() * 1000)
        try:
            with PiCamera(resolution=(self.width, self.height), framerate=self.framerate) as camera:
                stream = np.empty(
                    (self.height, self.width, CHANNELS), dtype=np.uint8)
                # capture frames from the camera
                for raw in camera.capture_continuous(stream, format="bgr", use_video_port=True):
                    frames += 1
                    frame = stream
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = self.classifier.detectMultiScale(
                        gray,
                        scaleFactor=scale_factor,
                        minNeighbors=min_neighbors,
                        minSize=tuple(min_size)
                    )
                    readings = [
                        {"Simple": {"name": "frontal_faces", "unit": "faces",
                            "value": float(len(faces))}},
                        {"Geometry": {"name": "classifier", "unit": "vector", "value":  list(map(
                            lambda f: {"Rectangle":{"x": int(f[0]), "y": int(f[1]), "w": int(f[2]), "h": int(f[3])}}, faces))}},
                        {"Tuple": {"name": "image", "unit": "pixels",
                            "value": [self.width, self.height]}},

                    ]
                    data = (int(datetime.utcnow().timestamp() * 1000),
                            readings, "picam")
                    collector.collect(data)
                    if self.mark_faces:
                        for (x, y, w, h) in faces:
                            cv2.rectangle(frame, (x, y), (x + w, y + h),
                                          (0, 255, 0), 2)
                    self.last_frame = frame

                    if self._stop:
                        break
        finally:
            elapsed = int(datetime.utcnow().timestamp() * 1000) - start
            if elapsed >= 1000:
                logging.info("Ran for %d ms @ %d frames (%.2f fps)" %
                             (elapsed, frames, frames / int(elapsed / 1000)))
