from twExceptions.twExceptions import SensorConnectionException
from time import time
import asyncio
import Adafruit_GPIO.I2C as I2C
from twABCs.sensor import Sensor


class TSL2561(Sensor):
    TSL2561_I2CADDR = 0x49  # 0x39
    ADC_CHANNEL0_LOW = 0x8C
    ADC_CHANNEL1_LOW = 0x8E

    ITIME_100 = 0x00  # Integrationszeit [ms]
    ITIME_200 = 0x01
    ITIME_300 = 0x02
    ITIME_400 = 0x03
    ITIME_500 = 0x04
    ITIME_600 = 0x05

    GAIN_REG = 0x81

    GAIN_LOW = 0x00  # low gain (1x)
    GAIN_MED = 0x10  # medium gain (25x)
    GAIN_HIGH = 0x20  # high gain (428x)
    GAIN_MAX = 0x30  # maximum gain (9876x)

    def __init__(self, controller, timeout=1, address= TSL2561_I2CADDR, bus=1, name="L1", gain=0):
        super().__init__()
        self._controller = controller
        controller.register_sensor(self, name)
        self._timeout = timeout
        self._run = False
        self._active = False
        self._name = name
        self._device = I2C.get_i2c_device(address, busnum=bus)
        self._gain = gain

    def set_gain(self, gain=1):
        """ Set the gain """
        if gain != self._gain:
            if gain == 1:                           #high resolution / scale 1.0
                self._device.write8(self.GAIN_REG, 0x02)     # set gain = 1X and timing = 402 mSec
            else:                                   #
                self._device.write8(self.GAIN_REG, 0x12)     # set gain = 16X and timing = 402 mSec
            self._gain = gain                     # safe gain for calculation
            time.sleep(1)              # pause for integration (self.pause must be bigger than integration time)

    def read_byte(self, addr):
        datal = self._device.readU8(addr)
        datah = self._device.readU8(addr+1)
        channel = 256 * datah + datal
        return channel

    def read_ambient(self, reg= ADC_CHANNEL0_LOW):
        """Reads visible+IR diode from the I2C device"""
        return self.read_byte(reg)

    def read_ir(self, reg=ADC_CHANNEL1_LOW):
        """Reads IR only diode from the I2C device"""
        return self.read_byte(reg)

    def _get_data(self):
        if self._gain == 1:
            ambient = self.read_ambient()
            IR = self.read_ir()
            ambient *= 16  # scale 1x to 16x
            IR *= 16  # scale 1x to 16x

        elif self._gain == 16:
            ambient = self.read_ambient()
            IR = self.read_ir()

        elif self._gain == 0:
            ambient = self.read_ambient()
            if ambient < 65535:
                IR = self.read_ir()
            if ambient >= 65535 or IR >= 65535:  # value(s) exeed(s) datarange
                ambient = self.read_ambient()
                IR = self.read_ir()

        return IR, ambient

    def _convert_to_lux(self, ir, ambient):
        try:
            ratio = (ir / float(ambient))
        except ZeroDivisionError:
            ratio = 2.0

        if (ratio >= 0) & (ratio <= 0.52):
            lux = (0.0315 * ambient) - (0.0593 * ambient * (ratio**1.4))
        elif ratio <= 0.65:
            lux = (0.0229 * ambient) - (0.0291 * ir)
        elif ratio <= 0.80:
            lux = (0.0157 * ambient) - (0.018 * ir)
        elif ratio <= 1.3:
            lux = (0.00338 * ambient) - (0.0026 * ir)
        elif ratio > 1.3:
            lux = 0
        else:
            return

        return lux

    def check(self):
        return True

    def _measure_value(self):
        """"Read sensor Pixels and return its values in lux."""
        data = self._get_data()
        ambient = data[1]
        ir = data[0]
        val = self._convert_to_lux(ir, ambient)
        print(val)
        return val

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
        self._device.write8(0x80, 0x03)  # 0x81 ?                    power up the device
        asyncio.set_event_loop(loop)
        loop.create_task(self._measure_continuously())
        return None

    def stop(self):
        self._run = False
        self._device.write8(0x80, 0x00)  # 0x81 ?                    shut down the device
        return True
