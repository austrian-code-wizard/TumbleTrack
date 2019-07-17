from twExceptions.twExceptions import SensorConnectionException
from time import time
import asyncio
import Adafruit_GPIO.I2C as I2C
from twABCs.sensor import Sensor
from twTesting import device_tests

class AMG8833(Sensor):
    AMG88xx_I2CADDR = 0x68  # sonst 0x69
    AMG88xx_DEFAULT_BUS = 1
    AMG88xx_PCTL = 0x00
    AMG88xx_RST = 0x01
    AMG88xx_FPSC = 0x02
    AMG88xx_INTC = 0x03
    AMG88xx_STAT = 0x04
    AMG88xx_SCLR = 0x05

    # 0x06 reserved
    AMG88xx_AVE = 0x07
    AMG88xx_INTHL = 0x08
    AMG88xx_INTHH = 0x09
    AMG88xx_INTLL = 0x0A
    AMG88xx_INTLH = 0x0B
    AMG88xx_IHYSL = 0x0C
    AMG88xx_IHYSH = 0x0D
    AMG88xx_TTHL = 0x0E
    AMG88xx_TTHH = 0x0F
    AMG88xx_INT_OFFSET = 0x010
    AMG88xx_PIXEL_OFFSET = 0x80  # ends at 0xFF

    # Operating Modes
    AMG88xx_NORMAL_MODE = 0x00
    AMG88xx_SLEEP_MODE = 0x01
    AMG88xx_STAND_BY_60 = 0x20
    AMG88xx_STAND_BY_10 = 0x21

    # sw resets
    AMG88xx_FLAG_RESET = 0x30
    AMG88xx_INITIAL_RESET = 0x3F

    # frame rates
    AMG88xx_FPS_10 = 0x00
    AMG88xx_FPS_1 = 0x01

    # int enables
    AMG88xx_INT_DISABLED = 0x00
    AMG88xx_INT_ENABLED = 0x01

    # int modes
    AMG88xx_DIFFERENCE = 0x00
    AMG88xx_ABSOLUTE_VALUE = 0x01

    AMG88xx_PIXEL_ARRAY_SIZE = 64
    AMG88xx_PIXEL_TEMP_CONVERSION = .25
    AMG88xx_THERMISTOR_CONVERSION = .0625

    def __init__(self, controller, timeout=1, address=AMG88xx_I2CADDR, bus=1, name="IR1"):
        super().__init__()
        self._controller = controller
        controller.register_sensor(self, name)
        self._timeout = timeout
        self._run = False
        self._active = False
        self._name = name
        self._device = I2C.get_i2c_device(address, busnum=bus)

    def check(self):
        check = device_tests.device_tests(self, self._name)
        return check.basic_check()

    def _measure_value(self):
        """Read sensor Pixels and return its values in degrees celsius."""
        # Read temperature register value.
        data = []
        for i in range(0, AMG8833.AMG88xx_PIXEL_ARRAY_SIZE):
            raw = self._device.readU16(AMG8833.AMG88xx_PIXEL_OFFSET + (i << 1))
            if raw & 0x7FF != raw:
                raw -= 4096
            data.append(raw * AMG8833.AMG88xx_PIXEL_TEMP_CONVERSION)
        return data

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
