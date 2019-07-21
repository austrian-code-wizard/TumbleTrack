from twExceptions.twExceptions import TWException
from time import time
import asyncio
import random


class TestDevice:

	def __init__(self, controller, timeout=0.3, address=1, bus=1, name="TEST"):
		controller._devices[name] = self
		self._controller = controller
		self._timeout = timeout
		self._run = False
		self._active = False
		self._name = name


	def check(self):
		"""Start taking temperature measurements. Returns True if the device is
		intialized, False otherwise.
		"""

		# Check manufacturer and device ID match expected values.
		return True

	def _get_value(self):
		return random.randint(1, 1000)

	async def _measure_continuously(self):
		loop = asyncio.get_running_loop()
		self._active = True
		while self._run:
			end_time = time() + self._timeout
			result = await loop.run_in_executor(None, self._get_value)
			self._controller.receive_data(str(result), self._name)
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








