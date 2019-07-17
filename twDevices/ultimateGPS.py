from twExceptions.twExceptions import SensorConnectionException
from time import time
import asyncio
import gps
from twABCs.sensor import Sensor
from twTesting import device_tests


class UltimateGPS(Sensor):

	def __init__(self, controller, timeout=1, host="localhost", port="2947", name="G1"):
		super().__init__()
		self._controller = controller
		controller.register_sensor(self, name)
		self._timeout = timeout
		self._run = False
		self._active = False
		self._name = name
		self._device = gps.gps(host, port)
		self._device.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
		return

	def check(self) -> bool:
		check = device_tests.device_tests(self, self._name)
		return check.simple_check()

	def _measure_value(self) -> list:
		"""Read sensor and return its value in degrees celsius."""
		# Read temperature register value.
		data = self._device.next()
		results = []
		if data['class'] == 'TPV':
			if hasattr(data, 'time'):
				results.append(data.time)
			else:
				results.append(None)
			if hasattr(data, 'lon'):
				results.append(data.lon)
			else:
				results.append(None)
			if hasattr(data, 'lat'):
				results.append(data.lat)
			else:
				results.append(None)
			if hasattr(data, 'speed'):
				results.append(data.speed)
			else:
				results.append(None)
		return results

	def get_single_measurement(self) -> list:
		return self._measure_value()

	async def _measure_continuously(self) -> bool:
		loop = asyncio.get_running_loop()
		self._active = True
		while self._run:
			end_time = time() + self._timeout
			result = await loop.run_in_executor(None, self._measure_value)
			self._controller.receive_data(str(result), self._name)
			delta_time = end_time - time()
			if delta_time > 0:
				await asyncio.sleep(delta_time)
		self._active = False
		return True

	def start(self, loop: asyncio.AbstractEventLoop) -> bool:
		self._run = True
		asyncio.set_event_loop(loop)
		loop.create_task(self._measure_continuously())
		return True

	def stop(self) -> bool:
		self._run = False
		return True
