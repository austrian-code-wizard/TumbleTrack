from twExceptions.twExceptions import SensorConnectionException
from time import time
import asyncio
import Adafruit_GPIO.I2C as I2C
from twABCs.sensor import Sensor


class MCP9808(Sensor):
	# Default I2C address for device.
	MCP9808_I2CADDR_DEFAULT = 0x18
	MCP9808_I2C_BUS_DEFAULT = 1

	# Register addresses.
	MCP9808_REG_CONFIG = 0x01
	MCP9808_REG_UPPER_TEMP = 0x02
	MCP9808_REG_LOWER_TEMP = 0x03
	MCP9808_REG_CRIT_TEMP = 0x04
	MCP9808_REG_AMBIENT_TEMP = 0x05
	MCP9808_REG_MANUF_ID = 0x06
	MCP9808_REG_DEVICE_ID = 0x07

	# Configuration register values.
	MCP9808_REG_CONFIG_SHUTDOWN = 0x0100
	MCP9808_REG_CONFIG_CRITLOCKED = 0x0080
	MCP9808_REG_CONFIG_WINLOCKED = 0x0040
	MCP9808_REG_CONFIG_INTCLR = 0x0020
	MCP9808_REG_CONFIG_ALERTSTAT = 0x0010
	MCP9808_REG_CONFIG_ALERTCTRL = 0x0008
	MCP9808_REG_CONFIG_ALERTSEL = 0x0002
	MCP9808_REG_CONFIG_ALERTPOL = 0x0002
	MCP9808_REG_CONFIG_ALERTMODE = 0x0001

	def __init__(self, controller, timeout=1, address=MCP9808_I2CADDR_DEFAULT, bus=MCP9808_I2C_BUS_DEFAULT, name="T1"):
		super().__init__()
		self._controller = controller
		controller.register_sensor(self, name)
		self._timeout = timeout
		self._run = False
		self._active = False
		self._name = name
		self._device = I2C.get_i2c_device(address, busnum=bus)

	def check(self):
		"""Start taking temperature measurements. Returns True if the device is
		initialized, False otherwise.
		"""

		# Check manufacturer and device ID match expected values.
		mid = self._device.readU16BE(MCP9808.MCP9808_REG_MANUF_ID)
		did = self._device.readU16BE(MCP9808.MCP9808_REG_DEVICE_ID)
		if mid == 0x0054 and did == 0x0400:
			return True
		else:
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
