import Adafruit_GPIO.I2C as I2C
import time


class MPL3115A2:
	"""Instance of the MPL3115A2 sensor.  Must specify the following parameters
	when creating an instance of this device:
	- i2c: The I2C bus connected to the sensor.
	In addition you can specify the following optional keyword arguments:
	- address: The I2C address of the device if it's different from the default.
	"""

	# Class level buffer to reduce memory usage and allocations.
	# Note this is not thread safe by design!

	_MPL3115A2_BUS = 1
	_MPL3115A2_ADDRESS = 0x60
	_MPL3115A2_REGISTER_STATUS = 0x00
	_MPL3115A2_REGISTER_PRESSURE_MSB = 0x01
	_MPL3115A2_REGISTER_PRESSURE_CSB = 0x02
	_MPL3115A2_REGISTER_PRESSURE_LSB = 0x03
	_MPL3115A2_REGISTER_TEMP_MSB = 0x04
	_MPL3115A2_REGISTER_TEMP_LSB = 0x05
	_MPL3115A2_REGISTER_DR_STATUS = 0x06
	_MPL3115A2_OUT_P_DELTA_MSB = 0x07
	_MPL3115A2_OUT_P_DELTA_CSB = 0x08
	_MPL3115A2_OUT_P_DELTA_LSB = 0x09
	_MPL3115A2_OUT_T_DELTA_MSB = 0x0A
	_MPL3115A2_OUT_T_DELTA_LSB = 0x0B
	_MPL3115A2_WHOAMI = 0x0C
	_MPL3115A2_BAR_IN_MSB = 0x14
	_MPL3115A2_BAR_IN_LSB = 0x15

	_MPL3115A2_REGISTER_STATUS_TDR = 0x02
	_MPL3115A2_REGISTER_STATUS_PDR = 0x04
	_MPL3115A2_REGISTER_STATUS_PTDR = 0x08

	_MPL3115A2_PT_DATA_CFG = 0x13
	_MPL3115A2_PT_DATA_CFG_TDEFE = 0x01
	_MPL3115A2_PT_DATA_CFG_PDEFE = 0x02
	_MPL3115A2_PT_DATA_CFG_DREM = 0x04

	_MPL3115A2_CTRL_REG1 = 0x26
	_MPL3115A2_CTRL_REG2 = 0x27
	_MPL3115A2_CTRL_REG3 = 0x28
	_MPL3115A2_CTRL_REG4 = 0x29
	_MPL3115A2_CTRL_REG5 = 0x2A

	_MPL3115A2_CTRL_REG1_SBYB = 0x01
	_MPL3115A2_CTRL_REG1_OST = 0x02
	_MPL3115A2_CTRL_REG1_RST = 0x04
	_MPL3115A2_CTRL_REG1_RAW = 0x40
	_MPL3115A2_CTRL_REG1_ALT = 0x80
	_MPL3115A2_CTRL_REG1_BAR = 0x00

	_MPL3115A2_CTRL_REG1_OS1 = 0x00
	_MPL3115A2_CTRL_REG1_OS2 = 0x08
	_MPL3115A2_CTRL_REG1_OS4 = 0x10
	_MPL3115A2_CTRL_REG1_OS8 = 0x18
	_MPL3115A2_CTRL_REG1_OS16 = 0x20
	_MPL3115A2_CTRL_REG1_OS32 = 0x28
	_MPL3115A2_CTRL_REG1_OS64 = 0x30
	_MPL3115A2_CTRL_REG1_OS128 = 0x38

	_MPL3115A2_REGISTER_STARTCONVERSION = 0x12

	def __init__(self, address=_MPL3115A2_ADDRESS, busnum=_MPL3115A2_BUS):
		self._device = I2C.get_i2c_device(address, busnum=busnum)
		# Validate the chip ID.
		if self._device.readU8(MPL3115A2._MPL3115A2_WHOAMI) != 0xC4:
			raise RuntimeError('Failed to find MPL3115A2, check your wiring!')
		# Reset.  Note the chip immediately resets and won't send an I2C back
		# so we need to catch the OSError and swallow it (otherwise this fails
		# expecting an ACK that never comes).
		try:
			self._device.write8(MPL3115A2._MPL3115A2_CTRL_REG1, MPL3115A2._MPL3115A2_CTRL_REG1_RST)
		except OSError:
			pass
		time.sleep(0.01)
		# Poll for the reset to finish.
		self._poll_reg1(MPL3115A2._MPL3115A2_CTRL_REG1_RST)
		# Configure the chip registers with default values.
		self._ctrl_reg1 = MPL3115A2._MPL3115A2_CTRL_REG1_OS128 | MPL3115A2._MPL3115A2_CTRL_REG1_ALT
		self._device.write8(MPL3115A2._MPL3115A2_CTRL_REG1, self._ctrl_reg1)
		self._device.write8(MPL3115A2._MPL3115A2_PT_DATA_CFG, MPL3115A2._MPL3115A2_PT_DATA_CFG_TDEFE | \
											MPL3115A2._MPL3115A2_PT_DATA_CFG_PDEFE | \
											MPL3115A2._MPL3115A2_PT_DATA_CFG_DREM)

	def _poll_reg1(self, mask):
		# Poll the CTRL REG1 value for the specified masked bits to NOT be
		# present.
		while self._device.readU8(MPL3115A2._MPL3115A2_CTRL_REG1) & mask > 0:
			time.sleep(0.01)

	def reset(self):
		try:
			self._device.write8(MPL3115A2._MPL3115A2_CTRL_REG1, MPL3115A2._MPL3115A2_CTRL_REG1_RST)
		except OSError:
			pass
		time.sleep(0.01)
		# Poll for the reset to finish.
		self._poll_reg1(MPL3115A2._MPL3115A2_CTRL_REG1_RST)
		# Configure the chip registers with default values.
		self._ctrl_reg1 = MPL3115A2._MPL3115A2_CTRL_REG1_OS128 | MPL3115A2._MPL3115A2_CTRL_REG1_ALT
		self._device.write8(MPL3115A2._MPL3115A2_CTRL_REG1, self._ctrl_reg1)
		self._device.write8(MPL3115A2._MPL3115A2_PT_DATA_CFG, MPL3115A2._MPL3115A2_PT_DATA_CFG_TDEFE | \
											MPL3115A2._MPL3115A2_PT_DATA_CFG_PDEFE | \
											MPL3115A2._MPL3115A2_PT_DATA_CFG_DREM)

	def pressure(self):
		"""Read the barometric pressure detected by the sensor in Pascals."""
		# First poll for a measurement to be finished.
		self._poll_reg1(MPL3115A2._MPL3115A2_CTRL_REG1_OST)
		# Set control bits for pressure reading.
		self._ctrl_reg1 &= ~0b10000000  # Turn off bit 7, ALT.
		self._device.write8(MPL3115A2._MPL3115A2_CTRL_REG1, self._ctrl_reg1)
		self._ctrl_reg1 |= 0b00000010   # Set OST to 1 to start measurement.
		self._device.write8(MPL3115A2._MPL3115A2_CTRL_REG1, self._ctrl_reg1)
		# Poll status for PDR to be set.
		while self._device.readU8(MPL3115A2._MPL3115A2_REGISTER_STATUS) & MPL3115A2._MPL3115A2_REGISTER_STATUS_PDR == 0:
			time.sleep(0.01)
		pressure_msb = self._device.readU8(MPL3115A2._MPL3115A2_REGISTER_PRESSURE_MSB)
		pressure_csb = self._device.readU8(MPL3115A2._MPL3115A2_REGISTER_PRESSURE_CSB)
		pressure_lsb = self._device.readU8(MPL3115A2._MPL3115A2_REGISTER_PRESSURE_LSB)
		# Reconstruct 20-bit pressure value.
		pressure = ((pressure_msb << 16) | (pressure_csb << 8) | pressure_lsb) & 0xFFFFFF
		pressure >>= 4
		# Scale down to pascals.
		return pressure / 4.0

	def altitude(self):
		"""Read the altitude as calculated based on the sensor pressure and
		previously configured pressure at sea-level.  This will return a
		value in meters.  Set the sea-level pressure by updating the
		sealevel_pressure property first to get a more accurate altitude value.
		"""
		# First poll for a measurement to be finished.
		self._poll_reg1(MPL3115A2._MPL3115A2_CTRL_REG1_OST)
		# Set control bits for pressure reading.
		self._ctrl_reg1 |= 0b10000000  # Turn on bit 0, ALT.
		self._device.write8(MPL3115A2._MPL3115A2_CTRL_REG1, self._ctrl_reg1)
		self._ctrl_reg1 |= 0b00000010   # Set OST to 1 to start measurement.
		self._device.write8(MPL3115A2._MPL3115A2_CTRL_REG1, self._ctrl_reg1)
		# Poll status for PDR to be set.
		while self._device.readU8(MPL3115A2._MPL3115A2_REGISTER_STATUS) & MPL3115A2._MPL3115A2_REGISTER_STATUS_PDR == 0:
			time.sleep(0.01)
		alt_msb = self._device.readU8(MPL3115A2._MPL3115A2_REGISTER_PRESSURE_MSB)
		alt_csb = self._device.readU8(MPL3115A2._MPL3115A2_REGISTER_PRESSURE_CSB)
		alt_lsb = self._device.readU8(MPL3115A2._MPL3115A2_REGISTER_PRESSURE_LSB)
		altitude = (alt_msb << 24) | (alt_csb << 16) | (alt_lsb << 8)
		return altitude / 65535.0

	def temperature(self):
		"""Read the temperature as measured by the sensor in degrees Celsius.
		"""
		# Poll status for TDR to be set.
		while self._device.readU8(MPL3115A2._MPL3115A2_REGISTER_STATUS) & MPL3115A2._MPL3115A2_REGISTER_STATUS_TDR == 0:
			time.sleep(0.01)
		# Read 2 bytes of data from temp register.
		temp_msb = self._device.readU8(MPL3115A2._MPL3115A2_REGISTER_TEMP_MSB)
		temp_lsb = self._device.readU8(MPL3115A2._MPL3115A2_REGISTER_TEMP_LSB)
		temp = (temp_msb << 8) | temp_lsb
		temp >>= 4
		if temp & 0x800:
			temp |= 0xF000
		# Scale down to degrees Celsius.
		return temp / 16.0

if __name__ == "__main__":
	dev = MPL3115A2()
	print(dev.temperature())
	print(dev.pressure())
	print(dev.altitude())
