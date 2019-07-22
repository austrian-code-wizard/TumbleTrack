from twExceptions.twExceptions import SensorConnectionException
from time import time, sleep
import asyncio
import Adafruit_GPIO.I2C as I2C
from twABCs.sensor import Sensor
from twTesting import sensor_test


class ADS1115(Sensor):
	# Register and other configuration values:
	ADS1x15_DEFAULT_BUS = 1
	ADS1x15_DEFAULT_ADDRESS = 0x48
	ADS1x15_POINTER_CONVERSION = 0x00
	ADS1x15_POINTER_CONFIG = 0x01
	ADS1x15_POINTER_LOW_THRESHOLD = 0x02
	ADS1x15_POINTER_HIGH_THRESHOLD = 0x03
	ADS1x15_CONFIG_OS_SINGLE = 0x8000
	ADS1x15_CONFIG_MUX_OFFSET = 12
	# Mapping of gain values to config register values.
	ADS1x15_CONFIG_GAIN = {
		2 / 3: 0x0000,
		1: 0x0200,
		2: 0x0400,
		4: 0x0600,
		8: 0x0800,
		16: 0x0A00
	}
	PGA_RANGE = {
		2 / 3: 6.144,
		1: 4.096,
		2: 2.048,
		4: 1.024,
		8: 0.512,
		16: 0.256
	}
	ADS1x15_CONFIG_MODE_CONTINUOUS = 0x0000
	ADS1x15_CONFIG_MODE_SINGLE = 0x0100
	# Mapping of data/sample rate to config register values for ADS1115 (slower).
	ADS1115_CONFIG_DR = {
		8: 0x0000,
		16: 0x0020,
		32: 0x0040,
		64: 0x0060,
		128: 0x0080,
		250: 0x00A0,
		475: 0x00C0,
		860: 0x00E0
	}
	ADS1x15_CONFIG_COMP_WINDOW = 0x0010
	ADS1x15_CONFIG_COMP_ACTIVE_HIGH = 0x0008
	ADS1x15_CONFIG_COMP_LATCHING = 0x0004
	ADS1x15_CONFIG_COMP_QUE = {
		1: 0x0000,
		2: 0x0001,
		4: 0x0002
	}
	ADS1x15_CONFIG_COMP_QUE_DISABLE = 0x0003

	def __init__(self, controller, timeout=1, address=ADS1x15_DEFAULT_ADDRESS, bus=ADS1x15_DEFAULT_BUS, name="A1"):
		super().__init__()
		self._controller = controller
		controller.register_sensor(self, name)
		self._timeout = timeout
		self._run = False
		self._active = False
		self._name = name
		self._gain = 1
		self._data_rate = 128
		self._device = I2C.get_i2c_device(address, busnum=bus)

	def set_gain(self, gain):
		if gain not in ADS1115.ADS1x15_CONFIG_GAIN:
			raise ValueError  # TODO: raise tw specific error
		self._gain = gain

	def set_data_rate(self, data_rate):
		if data_rate not in ADS1115.ADS1115_CONFIG_DR:
			raise ValueError  # TODO: raise tw specific error
		self._data_rate = data_rate

	def check(self):
		return True

	def _read(self, mux, gain, data_rate, mode):
		"""Perform an ADC read with the provided mux, gain, data_rate, and mode
		values.  Returns the signed integer result of the read.
		"""
		config = ADS1115.ADS1x15_CONFIG_OS_SINGLE  # Go out of power-down mode for conversion.
		# Specify mux value.
		config |= (mux & 0x07) << ADS1115.ADS1x15_CONFIG_MUX_OFFSET
		# Validate the passed in gain and then set it in the config.
		if gain not in ADS1115.ADS1x15_CONFIG_GAIN:
			raise ValueError('Gain must be one of: 2/3, 1, 2, 4, 8, 16')
		config |= ADS1115.ADS1x15_CONFIG_GAIN[gain]
		# Set the mode (continuous or single shot).
		config |= mode
		# Get the default data rate if none is specified (default differs between
		# ADS1015 and ADS1115).
		if data_rate is None:
			data_rate = self._data_rate_default()
		# Set the data rate (this is controlled by the subclass as it differs
		# between ADS1015 and ADS1115).
		config |= self._data_rate_config(data_rate)
		config |= ADS1115.ADS1x15_CONFIG_COMP_QUE_DISABLE  # Disble comparator mode.
		# Send the config value to start the ADC conversion.
		# Explicitly break the 16-bit value down to a big endian pair of bytes.
		self._device.writeList(ADS1115.ADS1x15_POINTER_CONFIG, [(config >> 8) & 0xFF, config & 0xFF])
		# Wait for the ADC sample to finish based on the sample rate plus a
		# small offset to be sure (0.1 millisecond).
		sleep(1.0 / data_rate + 0.0001)
		# Retrieve the result.
		result = self._device.readList(ADS1115.ADS1x15_POINTER_CONVERSION, 2)
		return self._conversion_value(result[1], result[0])

	@staticmethod
	def _data_rate_default():
		# Default from datasheet page 16, config register DR bit default.
		return 128

	@staticmethod
	def _data_rate_config(data_rate):
		if data_rate not in ADS1115.ADS1115_CONFIG_DR:
			raise ValueError('Data rate must be one of: 8, 16, 32, 64, 128, 250, 475, 860')
		return ADS1115.ADS1115_CONFIG_DR[data_rate]

	@staticmethod
	def _conversion_value(low, high):
		# Convert to 16-bit signed value.
		value = ((high & 0xFF) << 8) | (low & 0xFF)
		# Check for sign bit and turn into a negative value if set.
		if value & 0x8000 != 0:
			value -= 1 << 16
		return value

	def _measure_value(self):
		results = []
		for channel in range(0, 4):
			value = self._read(channel + 0x04, self._gain, self._data_rate, ADS1115.ADS1x15_CONFIG_MODE_SINGLE)
			value = value * ADS1115.PGA_RANGE[self._gain] / 2**15
			results.append(value)
		return results

	def _measure_channel_value(self, channel):
		if channel not in [0, 1, 2, 3]:
			raise ValueError  # TODO: raise tw specific error
		raw_value = self._read(channel + 0x04, self._gain, self._data_rate, ADS1115.ADS1x15_CONFIG_MODE_SINGLE)
		return raw_value * ADS1115.PGA_RANGE[self._gain] / 2**15

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
