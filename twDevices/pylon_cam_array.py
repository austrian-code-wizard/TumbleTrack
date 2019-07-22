import asyncio
from time import time
import uuid

from twABCs.sensor import Sensor
from twABCs.controller import Controller
from twTesting import sensor_test
from pypylon import pylon
import numpy as np

# TODO


class PylonCamArray(Sensor):

    def __init__(self, controller: Controller, binning_factor=4, max_cam_count=10, acquisition_timeout=1000, retrieval_timeout=5000, timeout=1):
        super().__init__()
        self._controller = controller
        self._camera_id = f'camera_{uuid.uuid4()}'
        controller.register_sensor(self, self._camera_id)
        self._acquisition_timeout = acquisition_timeout
        self._retrieval_timeout = retrieval_timeout
        self._timeout = timeout

        self._run = False
        self._active = False

        self._tl_factory = pylon.TlFactory.GetInstance()
        devices = self._tl_factory.EnumerateDevices()
        if len(devices) == 0:
            raise pylon.RuntimeException('No cameras attached.')
        self._cameras = pylon.InstantCameraArray(min(len(devices), max_cam_count))

        for i, cam in enumerate(self._cameras):
            cam.Attach(self._tl_factory.CreateDevice(devices[i]))
            # Print the model name of the camera.
            print("Using device ", cam.GetDeviceInfo().GetModelName())

        self._camera.PixelFormat = "RGB8"
        self._camera.BinningHorizontal = binning_factor
        self._camera.BinningVertical = binning_factor

    def check(self) -> bool:
        pass

    def start_supervised_check(self):
        for i, cam in enumerate(self._cameras):
            print(f'Camera {i}', cam.GetDeviceInfo().GetModelName())

        # TODO test patterns, isopen,..

    def _measure_value(self):
        raise NotImplementedError

    def get_single_measurement(self):
        raise NotImplementedError

    async def _measure_continuously(self):
        pass

    def start(self, loop):
        pass

    def stop(self) -> bool:
        pass