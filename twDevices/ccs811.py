from twExceptions.twExceptions import SensorConnectionException
from time import time
import asyncio
import Adafruit_GPIO.I2C as I2C
from twDevices.mcp9808 import MCP9808
from twABCs.sensor import Sensor
from twTesting import sensor_test as Test


class CCS811(Sensor):

	CCS811_BUS = 1
	CCS811_ADDRESS = 0x5A

	_ALG_RESULT_DATA = 0x02
	_RAW_DATA = 0x03
	_ENV_DATA = 0x05
	_NTC = 0x06
	_THRESHOLDS = 0x10

	_BASELINE = 0x11
	_HW_ID = 0x20
	_HW_VERSION = 0x21
	_FW_BOOT_VERSION = 0x23
	_FW_APP_VERSION = 0x24
	_ERROR_ID = 0xE0

	_SW_RESET = 0xFF

	_BOOTLOADER_APP_ERASE = 0xF1
	_BOOTLOADER_APP_DATA = 0xF2
	_BOOTLOADER_APP_VERIFY = 0xF3
	_BOOTLOADER_APP_START = 0xF4

	DRIVE_MODE_IDLE = 0x00
	DRIVE_MODE_1SEC = 0x01
	DRIVE_MODE_10SEC = 0x02
	DRIVE_MODE_60SEC = 0x03
	DRIVE_MODE_250MS = 0x04

	_HW_ID_CODE = 0x81
	_REF_RESISTOR = 100000

	def __init__(self, controller, timeout=1, address=CCS811_ADDRESS, bus=CCS811_BUS, name="C1"):
		super().__init__()
		self._controller = controller
		controller.register_sensor(self, name)
		self._timeout = timeout
		self._run = False
		self._active = False
		self._name = name
		self._device = I2C.get_i2c_device(address, busnum=bus)

	def check(self):
		try:
			mid = self._device.readU16BE(MCP9808.MCP9808_REG_MANUF_ID)
			did = self._device.readU16BE(MCP9808.MCP9808_REG_DEVICE_ID) # TODO implement this test in sensor_test
			data = self.get_single_measurement()
			data_types = 'temperature'
			test = Test.sensor_test(self, self._name)
			result = test.test_data(data_types, data)
			return result
		except IOError:
			print(self._name + "not connected")
			return False

	def _measure_value(self):
		"""Read sensor and return its value in degrees celsius."""
		# Read temperature register value.
		t = self._device.readU16BE(MCP9808.MCP9808_REG_AMBIENT_TEMP)
		# Scale and convert to signed value.
		temp = (t & 0x0FFF) / 16.0
		if t & 0x1000:
			temp -= 256.0
		return temp

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
