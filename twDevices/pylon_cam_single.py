import asyncio
from time import time
import uuid

from twABCs.sensor import Sensor
from twABCs.controller import Controller
from twTesting import sensor_test
from pypylon import pylon
import numpy as np


class PylonCamSingle(Sensor):

    def __init__(self, controller: Controller, binning_factor=4, acquisition_timeout=1000, retrieval_timeout=5000, timeout=1):
        super().__init__()
        self._controller = controller
        self._camera_id = f'camera_{uuid.uuid4()}'
        controller.register_sensor(self, self._camera_id)
        self._acquisition_timeout = acquisition_timeout
        self._retrieval_timeout = retrieval_timeout
        self._timeout = timeout

        self._run = False
        self._active = False

        self._camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self._camera.Open()

        self._camera.PixelFormat = "RGB8"
        self._camera.BinningHorizontal = binning_factor
        self._camera.BinningVertical = binning_factor

    def check(self) -> bool:
        return True

    def start_supervised_check(self) -> np.ndarray:
        print("Using device ", self._camera.GetDeviceInfo().GetModelName())
        self._camera.TestPattern = "ColorDiagonalSawtooth8"
        for i in range(20):
            result = self._camera.GrabOne(self._acquisition_timeout)
            if result.GrabSucceeded():
                return result.Array

        raise pylon.TimeoutException()

    def _measure_value(self):
        self._camera.StartGrabbingMax(1)

    def get_single_measurement(self):
        self._measure_value()
        grab_result = self._camera.RetrieveResult(self._retrieval_timeout, pylon.TimeoutHandling_ThrowException)

        if grab_result.GrabSucceeded():
            img = grab_result.Array
            grab_result.Release()
            return img
        else:
            raise pylon.RuntimeException('Image acquisition failed')

    async def _measure_continuously(self):
        loop = asyncio.get_running_loop()
        self._active = True
        while self._run:
            end_time = time() + self._timeout
            result = await loop.run_in_executor(None, self._measure_value())
            self._controller.receive_data(result, self._camera_id)
            delta_time = end_time - time()
            if delta_time > 0:
                await asyncio.sleep(delta_time)
        self._active = False
        return True

    def start(self, loop):
        self._run = True
        asyncio.set_event_loop(loop)
        loop.create_task(self._measure_continuously())
        return None

    def stop(self):
        self._run = False
        return True