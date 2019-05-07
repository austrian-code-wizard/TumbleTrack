from functools import wraps


def register_command(func):
	@wraps(func)
	def method(*args, **kwargs):
		a = 1
		print(a)
		return func(*args, **kwargs)
	return method



class ActionHandler:

	def __init__(self):
		self._subjects = []
		self._commands = []
		self._command_type_flag = "T"

	def _get_command_type(self, packet):
		pass

	def _get_command_subject(self, packet):
		pass

	def _get_command_params(self, packet):
		pass

	@classmethod
	@register_command
	def stop(cls, subject):
		pass

	def handle_command(self, packet):
		command = self._get_command(packet)
		subject = self._get_command_subject(packet)
		params = self._get_command_params(packet)
		return command(subject, params)


if __name__ == "__main__":
	pass
