import serial
from twExceptions.twExceptions import TWException
from time import sleep

"""

async new message:
	if new_message:
		send(42)
		while not sent:
			if length of buffer > 0:
				response = read 1 byte (ergbenis ist 42 oder 43)
				if response is 42:
					send_message
				if response is 43 (arduino wants to send):
					receive and handle message
	else:
		if length of buffer > 0:
			response = 1 byte (ergebnis ist 43)
			if 43:
				receive message
			else:
				nothing
"""

class ArduinoSerial:
	def __init__(self, start_flag, end_flag, port=None) -> None:
		self._baud = 9600
		self._port = port
		self._start_flag = start_flag
		self._end_flag = end_flag
		self._arduino_ready_to_receive = b'\x2a'
		self._arduino_wants_to_send = b'\x2b'
		self._serial_port = None

	def receive(self) -> str:
		message = ""
		while True:
			new_char = (self._serial_port.read(1)).decode()
			if new_char == self._start_flag:
				length = (self._serial_port.read(1))[0]
				assert (self._serial_port.read(1)).decode() == self._start_flag
				for i in range(0, length):
					new_char = self._serial_port.read(1)
					message += new_char.decode()
				assert (self._serial_port.read(1)).decode() == self._end_flag
				return message

	def new_data_available(self):
		if self._serial_port.in_waiting > 0:
			return True
		else:
			return False

	def request_to_send(self):
		self._serial_port.write(self._arduino_ready_to_receive)
		return True

	def ready_to_receive(self):
		if self._serial_port.in_waiting > 0:
			new_char = self._serial_port.read(1)
			if new_char == self._arduino_ready_to_receive:
				return True
			elif new_char == self._arduino_wants_to_send:
				return False
			else:
				return False
				#raise TWException("Invalid response from arduino")
		else:
			return False

	def ready_to_send(self):
		if self._serial_port.in_waiting > 0:
			new_char = self._serial_port.read(1)
			if new_char == self._arduino_wants_to_send:
				return True
			else:
				return False
		else:
			return False

	def write(self, message: bytes) -> bool:
		if self._serial_port is None:
			return False # TODO: handle properly
		try:
			self._serial_port.write(self._start_flag.encode()+bytes([(len(message))]))
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
			sleep(0.8)
			return True
		except Exception as e:
			print(e)  # TODO: add logger
			self._serial_port = None
			return False

	def is_connected(self):
		if self._serial_port is None:
			return False
		elif isinstance(self._serial_port, serial.Serial):
			return True
		else:
			ValueError("Invalid value for arduino serial port")
