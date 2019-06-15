from twExceptions.twExceptions import SensorConnectionException
from time import time
import asyncio
import serial
import struct
from twABCs.sensor import Sensor


class PMS5003(Sensor):

	# Byte commands to control the PMS
	_PASSIVE_READ = b'\x42\x4d\xe2\x00\x00\x01\x71'
	_PASSIVE_MODE = b'\x42\x4d\xe1\x00\x00\x01\x70'
	_ACTIVE_MODE = b'\x42\x4d\xe1\x00\x01\x01\x71'
	_SLEEP = b'\x42\x4d\xe4\x00\x00\x01\x73'
	_WAKEUP = b'\x42\x4d\xe4\x00\x01\x01\x74'

	def __init__(self, controller, timeout=2, address="/dev/ttyUSB0", baud_rate=9600, name="D1"):
		super().__init__()
		self._controller = controller
		controller.register_sensor(self, name)
		self._timeout = timeout
		self._run = False
		self._active = False
		self._name = name
		self._device = serial.Serial(address, baud_rate)

	def check(self):
		self._device.write(PMS5003._PASSIVE_MODE)
		self._device.flushInput()
		return True

	def _measure_value(self) -> list:
		"""Read sensor and return its value in degrees celsius."""
		# Read temperature register value.
		self._device.write(PMS5003._PASSIVE_READ)
		data = self._device.read(32)
		if len(data) != 32 and not data.startswith(b'BM'):
			raise ValueError('Unable to read from PMS')
		items = struct.unpack('>HHHHHHHHHHHHHHHH', data)
		cksum = sum(data[0:30])
		if cksum != items[-1]:
			raise ValueError('Checksum missmatch')
		results = []
		for result in range(2, 14):
			results.append(float(items[result]))
		return results

	def get_single_measurement(self):
		return self._measure_value()

	async def _measure_continuously(self):
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

	def start(self, loop):
		self._run = True
		asyncio.set_event_loop(loop)
		loop.create_task(self._measure_continuously())
		return None

	def stop(self):
		self._run = False
		return True
