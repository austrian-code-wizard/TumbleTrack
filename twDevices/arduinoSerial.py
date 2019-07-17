import serial
from twTesting import device_tests


class ArduinoSerial:
	def __init__(self, start_flag, end_flag, port=None) -> None:
		self._baud = 9600
		self._port = port
		self._start_flag = start_flag
		self._end_flag = end_flag
		self._serial_port = None

	def receive(self) -> str:
		reading = False
		message = ""
		while True:
			new_char = (self._serial_port.read(1)).decode()
			if new_char == self._start_flag and reading is False:
				reading = True
			elif new_char == self._end_flag and reading is True:
				return message
			elif reading is True:
				message += new_char

	def write(self, message: bytes) -> bool:
		if self._serial_port is None:
			return False # TODO: handle properly
		try:
			print(f"writing: {message}")
			self._serial_port.write(message)
			return True
		except:
			return False  # TODO: handle properly

	def connect(self, port=None):
		try:
			if port is not None:
				self._port = port
			elif self._port is None:
				return False  # TODO: handle properly
			self._serial_port = serial.Serial(port=self._port, baudrate=self._baud)
			return True
		except Exception as e:
			print(e)  # TODO: add logger
			self._serial_port = None
			return False
