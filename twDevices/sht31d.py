from time import time, sleep
import asyncio
import Adafruit_GPIO.I2C as I2C
from twABCs.sensor import Sensor
from twTesting import sensor_test
SHT31_DEFAULT_BUS = 1
SHT31_I2CADDR = 0x44

SHT31_MEAS_HIGHREP_STRETCH = 0x2C06
SHT31_MEAS_MEDREP_STRETCH = 0x2C0D
SHT31_MEAS_LOWREP_STRETCH = 0x2C10
SHT31_MEAS_HIGHREP = 0x2400
SHT31_MEAS_MEDREP = 0x240B
SHT31_MEAS_LOWREP = 0x2416
SHT31_READSTATUS = 0xF32D
SHT31_CLEARSTATUS = 0x3041
SHT31_SOFTRESET = 0x30A2
SHT31_HEATER_ON = 0x306D
SHT31_HEATER_OFF = 0x3066

SHT31_STATUS_DATA_CRC_ERROR = 0x0001
SHT31_STATUS_COMMAND_ERROR = 0x0002
SHT31_STATUS_RESET_DETECTED = 0x0010
SHT31_STATUS_TEMPERATURE_ALERT = 0x0400
SHT31_STATUS_HUMIDITY_ALERT = 0x0800
SHT31_STATUS_HEATER_ACTIVE = 0x2000
SHT31_STATUS_ALERT_PENDING = 0x8000


class SHT31D(Sensor):

    def __init__(self, controller, timeout=1, address=SHT31_I2CADDR, bus=SHT31_DEFAULT_BUS, name="HT1"):
        super().__init__()
        self._controller = controller
        controller.register_sensor(self, name)
        self._timeout = timeout
        self._run = False
        self._active = False
        self._name = name
        self._device = I2C.get_i2c_device(address, busnum=bus)
        self.hum = True

    def set_mode(self, bol=0):
        self.hum = bol

    def check(self) -> bool:
        #check = sensor_test.sensor_test(self, self._name)
        #return check.full_check()
        return True

    def _measure_value(self):
        self._device.write8(SHT31_MEAS_HIGHREP >> 8, SHT31_MEAS_HIGHREP & 0xFF)
        time.sleep(0.015)
        buffer = self._device.readList(0, 6)

        if buffer[2] != self._crc8(buffer[0:2]):
            return float("nan"), float("nan")

        raw_temperature = buffer[0] << 8 | buffer[1]
        temperature = 175.0 * raw_temperature / 0xFFFF - 45.0

        if buffer[5] != self._crc8(buffer[3:5]):
            return float("nan"), float("nan")

        raw_humidity = buffer[3] << 8 | buffer[4]
        humidity = 100.0 * raw_humidity / 0xFFFF
        print(humidity, temperature)
        if self.hum:
            return humidity
        return temperature

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

    def stop(self) -> bool:
        self._run = False
        return True

    def _crc8(self, buffer):
        """ Polynomial 0x31 (x8 + x5 +x4 +1) """

        polynomial = 0x31;
        crc = 0xFF;

        index = 0
        for index in range(0, len(buffer)):
            crc ^= buffer[index]
            for i in range(8, 0, -1):
                if crc & 0x80:
                    crc = (crc << 1) ^ polynomial
                else:
                    crc = (crc << 1)
        return crc & 0xFF
