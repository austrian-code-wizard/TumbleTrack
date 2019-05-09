class TestController:
	def __init__(self):
		self._messages = []

	def handle_command(self, data: str) -> bool:
		self._messages.append(data)
		print(data)
		return True

	def get_messages(self) -> list:
		messages = self._messages
		self._messages = []
		return messages
