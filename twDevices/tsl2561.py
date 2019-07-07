from twExceptions.twExceptions import SensorConnectionException
from time import time
import asyncio
import Adafruit_GPIO.I2C as I2C
from twABCs.sensor import Sensor
# ausschalten  i2cset -y 1 0x39 0x80 0x00
# einschalten  i2cset -y 1 0x39 0x80 0x03


class TSL2561(Sensor):
    TSL2561_I2CADDR = 0x49  # 0x39
    DATA_ADDR_LOW = 0xC
    DATA_ADDR_HIGH = 0xF

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
        self._debug = 0

    """
    def set_gain(self, itime, gain=0x02):
        """ "Set the gain" """
        gain = gain | itime
        if gain != self._gain:
            if gain == 1:                           #high resolution / scale 1.0
                self._device.write8(self.GAIN_REG, 0x02)     # set gain = 1X and timing = 402 mSec
                if self._debug:
                    print("Setting low gain")
            else:                                   #
                self._device.write8(self.GAIN_REG, 0x12)     # set gain = 16X and timing = 402 mSec
                if self._debug:
                    print("Setting high gain")
            self._gain = gain                     # safe gain for calculation
            # time.sleep(1)              # pause for integration (self.pause must be bigger than integration time)
"""
    def set_gain(self, gain=1):
        """ "Set the gain" """
        if gain != self._gain:
            if gain == 1:                           #high resolution / scale 1.0
                self._device.write8(0x81, 0x02)     # set gain = 1X and timing = 402 mSec
                if self._debug:
                    print("Setting low gain")
            else:                                   #
                self._device.write8(0x81, 0x12)     # set gain = 16X and timing = 402 mSec
                if self._debug:
                    print("Setting high gain")
            self._gain = gain                     # safe gain for calculation
            # time.sleep(1)              # pause for integration (self.pause must be bigger than integration time)

    """def read_word(self, reg):
        """"Reads a word from the I2C device""""
        try:
            wordval = self._device.readU16(reg)
            newval = self.reverseByteOrder(wordval)
            if self._debug:
                print("I2C: Device 0x%02X returned 0x%04X from reg 0x%02X" )
            return newval
        except IOError:
            print("Error accessing 0x%02X: Check your I2C address" )
            return -1"""

    def read_word(self, addr=0xAC):
        data = self._device.readU16(addr)
        channel0 = 256 * data[0] + data[1]
        data = self._device.readU16(addr+2)
        channel1 = 256 * data[0] + data[1]
        return [channel0, channel1]

    def read_byte(self, addr=0x8C):
        datal = self._device.readU8(addr)
        datah = self._device.readU8(addr+1)
        channel = 256 * datah + datal
        return channel

    def read_fullself(self, reg=0x8C):
        """Reads visible+IR diode from the I2C device"""
        return self.read_byte(reg)

    def readIR(self, reg=0x8E):
        """Reads IR only diode from the I2C device"""
        return self.read_byte(reg)

    def read_lux(self, gain = 0):
        """Grabs a lux reading either with autoranging (gain=0) or with a specified gain (1, 16)"""
        if gain == 1 or gain == 16:
            self.set_gain(gain)  # low/highGain
            ambient = self.read_fullself()
            IR = self.readIR()
        elif gain==0: # auto gain
            self.set_gain(16)  # first try highGain
            ambient = self.read_fullself()
            if ambient < 65535:
                IR = self.readIR()
            if ambient >= 65535 or IR >= 65535:  # value(s) exeed(s) datarange
                self.set_gain(1)  # set lowGain
                ambient = self.read_fullself()
                IR = self.readIR()
        else:
            print("Gain Value " + str(gain) +" not Valid")
            return

        if self._gain == 1:
           ambient *= 16    # scale 1x to 16x
           IR *= 16         # scale 1x to 16x

        ratio = (IR / float(ambient))  # changed to make it run under python 2

        if self._debug:
            print("IR Result", IR)
            print("Ambient Result", ambient)

        if (ratio >= 0) & (ratio <= 0.52):
            lux = (0.0315 * ambient) - (0.0593 * ambient * (ratio**1.4))
        elif ratio <= 0.65:
            lux = (0.0229 * ambient) - (0.0291 * IR)
        elif ratio <= 0.80:
            lux = (0.0157 * ambient) - (0.018 * IR)
        elif ratio <= 1.3:
            lux = (0.00338 * ambient) - (0.0026 * IR)
        elif ratio > 1.3:
            lux = 0
        else:
            return 
        print("LUX")
        return lux

    def check(self):
        return True

    def _measure_value(self):
        """"Read sensor Pixels and return its values in degrees celsius."""
        return self.read_lux()

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
        self._device.write8(0x80, 0x03)  # 0x81 ?                    power up the device
        return None

    def stop(self):
        self._run = False
        self._device.write8(0x80, 0x00)  # 0x81 ?                    power up the device
        return True