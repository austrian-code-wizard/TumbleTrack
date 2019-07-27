import random
import time


class TestSerial:

	def __init__(self, start_flag, end_flag, port=None) -> None:
		self._started = False
		self._new_data = True
		pass

	def receive(self) -> str:
		if not self._started:
			self._started = True
			return "start"
		else:
			if (random.randint(1, 100) % 5) == 0:
				return "confirm_test_message"
			else:
				return "pass"

	def write(self, message: bytes) -> bool:
		self._new_data = False
		print(f"I am sending: {message}")
		return True

	def connect(self, port=None):
		return True

	def is_connected(self):
		return True		# always connected

	def receive(self) -> str:
		return 'receiving test message'

	def new_data_available(self):
		self._new_data = random.randint(0,1) == 1
		return self._new_data

	def request_to_send(self):
		return self._new_data

	def ready_to_receive(self):
		return ~self._new_data

	def ready_to_send(self):
		return self._new_data

	def write(self, message: bytes) -> bool:
		print(message)
		return True

	def connect(self, port=None):
		time.sleep(0.8)
		return True
