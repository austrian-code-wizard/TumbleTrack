import random

class TestSerial:
	def __init__(self, start_flag, end_flag, port=None) -> None:
		self._started = False
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
		print(f"I am sending: {message}")
		return True

	def connect(self, port=None):
		return True

	def is_connected(self):
		return True		# always connected
