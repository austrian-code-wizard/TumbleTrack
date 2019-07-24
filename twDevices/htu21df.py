from twExceptions.twExceptions import SensorConnectionException
from time import time, sleep
import asyncio
import Adafruit_GPIO.I2C as I2C
from twABCs.sensor import Sensor
from twTesting import sensor_test as Test


class HTU21DF(Sensor):
	HTU21DF_BUS_DEFAULT = 1
	HTU21DF_I2C_ADDR = 0x40
	HTU21DF_READ_TEMP_HOLD = 0xE3
	HTU21DF_READ_HUM_HOLD = 0xE5
	HTU21DF_READ_TEMP_NO_HOLD = 0xF3
	HTU21DF_READ_HUM_NO_HOLD = 0xF5
	HTU21DF_WRITE_REG = 0xE6
	HTU21DF_READ_REG = 0xE7
	HTU21DF_RESET = 0xFE
	HTU21DF_RESET_REG_VALUE = 0x02

	def __init__(self, controller, timeout=1, address=HTU21DF_I2C_ADDR, bus=HTU21DF_BUS_DEFAULT, name="H1"):
		super().__init__()
		self._controller = controller
		controller.register_sensor(self, name)
		self._timeout = timeout
		self._run = False
		self._active = False
		self._name = name
		self._handler = None
		self._external_thermometer = "T1"
		self._device = I2C.get_i2c_device(address, busnum=bus)

	def check(self) -> bool:
		"""Check if sensor is connected properly
		"""
		try:
			self._device.writeRaw8(HTU21DF.HTU21DF_RESET)
			sleep(0.015)
			self._device.writeRaw8(HTU21DF.HTU21DF_READ_REG)
			if not self._device.readRaw8() == HTU21DF.HTU21DF_RESET_REG_VALUE:
				raise IOError("HTU21D-F device reset failed")  # TODO: user an tumbleweed specific error and implement this in sensor_test class

			data = self.get_single_measurement()
			data_types = 'humidity'
			test = Test.sensor_test(self, self._name)
			result = test.test_data(data_types, data)
			return result
		except IOError:
			print(self._name + "not connected")
			return False

	def _measure_value(self) -> float:
		"""Read sensor and return its value in humidity in percent."""
		self._device.writeRaw8(0xE5)
		res = self._device._bus._read_bytes(self._device._address, 3)
		h1 = res[0]
		h2 = res[1]
		humi_reading = (h1 * 256) + h2
		humi_reading = float(humi_reading)
		uncomp_humidity = ((humi_reading / 65536) * 125) - 6
		if self._handler is not None and self._handler.check_registered_objects(self._external_thermometer):
			temperature = self._handler.handle_packet(f"get_single_measurement+!{self._external_thermometer}")
		else:
			temperature = self._measure_temperature()
		humidity = ((25 - temperature) * -0.15) + uncomp_humidity
		return humidity

	def _measure_temperature(self) -> float:
		self._device.writeRaw8(0xE3)
		res = self._device._bus._read_bytes(self._device._address, 3)
		t1 = res[0]
		t2 = res[1]
		temp_reading = (t1 * 256) + t2
		temp_reading = float(temp_reading)
		temperature = ((temp_reading / 65536) * 175.72) - 46.85
		return temperature

	def get_single_measurement(self) -> float:
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

	def start(self, loop) -> bool:
		self._run = True
		asyncio.set_event_loop(loop)
		loop.create_task(self._measure_continuously())
		return True

	def stop(self) -> bool:
		self._run = False
		return True
