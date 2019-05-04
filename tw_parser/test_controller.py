class TestController:
	def __init__(self):
		self._messages = []

	def process_incoming_packet(self, data):
		self._messages.append(data)
		return True

	def get_messages(self):
		messages = self._messages
		self._messages = []
		return messages
