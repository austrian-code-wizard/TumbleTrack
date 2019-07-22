from twABCs.sensor import Sensor
from time import time, sleep
import asyncio
import Adafruit_GPIO.I2C as I2C

BNO055_I2C_ADDR = 0x28
BNO055_ID = 0xA0

# Power mode settings
POWER_MODE_NORMAL = 0X00
POWER_MODE_LOWPOWER = 0X01
POWER_MODE_SUSPEND = 0X02

# Operation mode settings
OPERATION_MODE_CONFIG = 0X00
OPERATION_MODE_ACCONLY = 0X01
OPERATION_MODE_MAGONLY = 0X02
OPERATION_MODE_GYRONLY = 0X03
OPERATION_MODE_ACCMAG = 0X04
OPERATION_MODE_ACCGYRO = 0X05
OPERATION_MODE_MAGGYRO = 0X06
OPERATION_MODE_AMG = 0X07
OPERATION_MODE_IMUPLUS = 0X08
OPERATION_MODE_COMPASS = 0X09
OPERATION_MODE_M4G = 0X0A
OPERATION_MODE_NDOF_FMC_OFF = 0X0B
OPERATION_MODE_NDOF = 0X0C

# Output vector type
VECTOR_ACCELEROMETER = 0x08
VECTOR_MAGNETOMETER = 0x0E
VECTOR_GYROSCOPE = 0x14
VECTOR_EULER = 0x1A
VECTOR_LINEARACCEL = 0x28
VECTOR_GRAVITY = 0x2E

# REGISTER DEFINITION START
BNO055_PAGE_ID_ADDR = 0X07

BNO055_CHIP_ID_ADDR = 0x00
BNO055_ACCEL_REV_ID_ADDR = 0x01
BNO055_MAG_REV_ID_ADDR = 0x02
BNO055_GYRO_REV_ID_ADDR = 0x03
BNO055_SW_REV_ID_LSB_ADDR = 0x04
BNO055_SW_REV_ID_MSB_ADDR = 0x05
BNO055_BL_REV_ID_ADDR = 0X06

# Accel data register
BNO055_ACCEL_DATA_X_LSB_ADDR = 0X08
BNO055_ACCEL_DATA_X_MSB_ADDR = 0X09
BNO055_ACCEL_DATA_Y_LSB_ADDR = 0X0A
BNO055_ACCEL_DATA_Y_MSB_ADDR = 0X0B
BNO055_ACCEL_DATA_Z_LSB_ADDR = 0X0C
BNO055_ACCEL_DATA_Z_MSB_ADDR = 0X0D

# Mag data register
BNO055_MAG_DATA_X_LSB_ADDR = 0X0E
BNO055_MAG_DATA_X_MSB_ADDR = 0X0F
BNO055_MAG_DATA_Y_LSB_ADDR = 0X10
BNO055_MAG_DATA_Y_MSB_ADDR = 0X11
BNO055_MAG_DATA_Z_LSB_ADDR = 0X12
BNO055_MAG_DATA_Z_MSB_ADDR = 0X13

# Gyro data registers
BNO055_GYRO_DATA_X_LSB_ADDR = 0X14
BNO055_GYRO_DATA_X_MSB_ADDR = 0X15
BNO055_GYRO_DATA_Y_LSB_ADDR = 0X16
BNO055_GYRO_DATA_Y_MSB_ADDR = 0X17
BNO055_GYRO_DATA_Z_LSB_ADDR = 0X18
BNO055_GYRO_DATA_Z_MSB_ADDR = 0X19

# Euler data registers
BNO055_EULER_H_LSB_ADDR = 0X1A
BNO055_EULER_H_MSB_ADDR = 0X1B
BNO055_EULER_R_LSB_ADDR = 0X1C
BNO055_EULER_R_MSB_ADDR = 0X1D
BNO055_EULER_P_LSB_ADDR = 0X1E
BNO055_EULER_P_MSB_ADDR = 0X1F

# Quaternion data registers
BNO055_QUATERNION_DATA_W_LSB_ADDR = 0x20
BNO055_QUATERNION_DATA_W_MSB_ADDR = 0x21
BNO055_QUATERNION_DATA_X_LSB_ADDR = 0x22
BNO055_QUATERNION_DATA_X_MSB_ADDR = 0x23
BNO055_QUATERNION_DATA_Y_LSB_ADDR = 0x24
BNO055_QUATERNION_DATA_Y_MSB_ADDR = 0x25
BNO055_QUATERNION_DATA_Z_LSB_ADDR = 0x26
BNO055_QUATERNION_DATA_Z_MSB_ADDR = 0x27

# Linear acceleration data registers
BNO055_LINEAR_ACCEL_DATA_X_LSB_ADDR = 0x28
BNO055_LINEAR_ACCEL_DATA_X_MSB_ADDR = 0x29
BNO055_LINEAR_ACCEL_DATA_Y_LSB_ADDR = 0x2A
BNO055_LINEAR_ACCEL_DATA_Y_MSB_ADDR = 0x2B
BNO055_LINEAR_ACCEL_DATA_Z_LSB_ADDR = 0x2C
BNO055_LINEAR_ACCEL_DATA_Z_MSB_ADDR = 0x2D

# Gravity data registers
BNO055_GRAVITY_DATA_X_LSB_ADDR = 0x2E
BNO055_GRAVITY_DATA_X_MSB_ADDR = 0x2F
BNO055_GRAVITY_DATA_Y_LSB_ADDR = 0x30
BNO055_GRAVITY_DATA_Y_MSB_ADDR = 0x31
BNO055_GRAVITY_DATA_Z_LSB_ADDR = 0x32
BNO055_GRAVITY_DATA_Z_MSB_ADDR = 0x33

# Temperature data register
BNO055_TEMP_ADDR = 0x34

# Status registers
BNO055_CALIB_STAT_ADDR = 0x35
BNO055_SELFTEST_RESULT_ADDR = 0x36
BNO055_INTR_STAT_ADDR = 0x37

BNO055_SYS_CLK_STAT_ADDR = 0x38
BNO055_SYS_STAT_ADDR = 0x39
BNO055_SYS_ERR_ADDR = 0x3A

# Unit selection register
BNO055_UNIT_SEL_ADDR = 0x3B
BNO055_DATA_SELECT_ADDR = 0x3C

# Mode registers
BNO055_OPR_MODE_ADDR = 0x3D
BNO055_PWR_MODE_ADDR = 0x3E

BNO055_SYS_TRIGGER_ADDR = 0x3F
BNO055_TEMP_SOURCE_ADDR = 0x40

# Axis remap registers
BNO055_AXIS_MAP_CONFIG_ADDR = 0x41
BNO055_AXIS_MAP_SIGN_ADDR = 0x42

# SIC registers
BNO055_SIC_MATRIX_0_LSB_ADDR = 0x43
BNO055_SIC_MATRIX_0_MSB_ADDR = 0x44
BNO055_SIC_MATRIX_1_LSB_ADDR = 0x45
BNO055_SIC_MATRIX_1_MSB_ADDR = 0x46
BNO055_SIC_MATRIX_2_LSB_ADDR = 0x47
BNO055_SIC_MATRIX_2_MSB_ADDR = 0x48
BNO055_SIC_MATRIX_3_LSB_ADDR = 0x49
BNO055_SIC_MATRIX_3_MSB_ADDR = 0x4A
BNO055_SIC_MATRIX_4_LSB_ADDR = 0x4B
BNO055_SIC_MATRIX_4_MSB_ADDR = 0x4C
BNO055_SIC_MATRIX_5_LSB_ADDR = 0x4D
BNO055_SIC_MATRIX_5_MSB_ADDR = 0x4E
BNO055_SIC_MATRIX_6_LSB_ADDR = 0x4F
BNO055_SIC_MATRIX_6_MSB_ADDR = 0x50
BNO055_SIC_MATRIX_7_LSB_ADDR = 0x51
BNO055_SIC_MATRIX_7_MSB_ADDR = 0x52
BNO055_SIC_MATRIX_8_LSB_ADDR = 0x53
BNO055_SIC_MATRIX_8_MSB_ADDR = 0x54
DATA_ADRESSES = {
    'temperature': BNO055_TEMP_ADDR,
    'quaternion': BNO055_QUATERNION_DATA_W_LSB_ADDR,
    'gravity': BNO055_GRAVITY_DATA_X_LSB_ADDR,
}
# Accelerometer Offset registers
ACCEL_OFFSET_X_LSB_ADDR = 0x55
ACCEL_OFFSET_X_MSB_ADDR = 0x56
ACCEL_OFFSET_Y_LSB_ADDR = 0x57
ACCEL_OFFSET_Y_MSB_ADDR = 0x58
ACCEL_OFFSET_Z_LSB_ADDR = 0x59
ACCEL_OFFSET_Z_MSB_ADDR = 0x5A

# Magnetometer Offset registers
MAG_OFFSET_X_LSB_ADDR = 0x5B
MAG_OFFSET_X_MSB_ADDR = 0x5C
MAG_OFFSET_Y_LSB_ADDR = 0x5D
MAG_OFFSET_Y_MSB_ADDR = 0x5E
MAG_OFFSET_Z_LSB_ADDR = 0x5F
MAG_OFFSET_Z_MSB_ADDR = 0x60

# Gyroscope Offset registers
GYRO_OFFSET_X_LSB_ADDR = 0x61
GYRO_OFFSET_X_MSB_ADDR = 0x62
GYRO_OFFSET_Y_LSB_ADDR = 0x63
GYRO_OFFSET_Y_MSB_ADDR = 0x64
GYRO_OFFSET_Z_LSB_ADDR = 0x65
GYRO_OFFSET_Z_MSB_ADDR = 0x66

# Radius registers
ACCEL_RADIUS_LSB_ADDR = 0x67
ACCEL_RADIUS_MSB_ADDR = 0x68
MAG_RADIUS_LSB_ADDR = 0x69
MAG_RADIUS_MSB_ADDR = 0x6A

class BNO05 (Sensor):

    def __init__(self, controller, timeout=1, address=BNO055_I2C_ADDR, bus=1, name="O1"):
        super().__init__()
        self._controller = controller
        controller.register_sensor(self, name)
        self._timeout = timeout
        self._run = False
        self._active = False
        self._name = name
        self._device = I2C.get_i2c_device(address, busnum=bus)
        self._reading_type = 'euler'

    def check(self) -> bool:
        # Make sure we have the right device
        if self._read_bytes(BNO05.BNO055_CHIP_ID_ADDR)[0] != BNO05.BNO055_ID:
            time.sleep(1)  # Wait for the device to boot up
            if self._read_bytes(BNO05.BNO055_CHIP_ID_ADDR)[0] != BNO05.BNO055_ID:
                return False    # TODO not finial refactor and redo this use sensor_test class

    def _measure_value(self):
        if self._reading_type == 'temperature':
            data = self._read_byte(BNO055_TEMP_ADDR)
            if data > 127:
                data -= 256
        elif self._reading_type == 'quaternion':
            w, x, y, z = self._read_vector(BNO055_QUATERNION_DATA_W_LSB_ADDR, 4)
            scale = (1.0 / (1 << 14))
            data = (x * scale, y * scale, z * scale, w * scale)
        elif self._reading_type == 'gravity':
            x, y, z = self._read_vector(BNO055_GRAVITY_DATA_X_LSB_ADDR)
            data = (x / 100.0, y / 100.0, z / 100.0)
        elif self._reading_type == 'linear_acceleration':
            x, y, z = self._read_vector(BNO055_LINEAR_ACCEL_DATA_X_LSB_ADDR)
            data = (x / 100.0, y / 100.0, z / 100.0)
        elif self._reading_type == 'accelerometer':
            x, y, z = self._read_vector(BNO055_ACCEL_DATA_X_LSB_ADDR)
            data = (x / 100.0, y / 100.0, z / 100.0)
        elif self._reading_type == 'gyroscope':
            x, y, z = self._read_vector(BNO055_GYRO_DATA_X_LSB_ADDR)
            data = (x / 900.0, y / 900.0, z / 900.0)
        elif self._reading_type == 'read_magnetometer':
            x, y, z = self._read_vector(BNO055_MAG_DATA_X_LSB_ADDR)
            data = (x / 16.0, y / 16.0, z / 16.0)
        elif self._reading_type == 'euler':
            heading, roll, pitch = self._read_vector(BNO055_EULER_H_LSB_ADDR)
            data = (heading / 16.0, roll / 16.0, pitch / 16.0)
        else:
            raise ValueError("Invalid data Type")
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

    def stop(self) -> bool:
        self._run = False
        return True

    def _read_vector(self, address, count=3):
        # Read count number of 16-bit signed values starting from the provided
        # address. Returns a tuple of the values that were read.
        data = self._read_bytes(address, count*2)
        result = [0]*count
        for i in range(count):
            result[i] = ((data[i*2+1] << 8) | data[i*2]) & 0xFFFF
            if result[i] > 32767:
                result[i] -= 65536
        return result

    def _read_bytes(self, address, length):
        return bytearray(self._device.readList(address, length))

    def _read_byte(self, address):
        # Read an 8-bit unsigned value from the provided register address.
        if self._device is not None:
            # I2C read.
            return self._device.readU8(address)
        else:
            return self._read_bytes(address, 1)[0]

    def writeBytes(self, register, value):
        self._device.write8(register, value)