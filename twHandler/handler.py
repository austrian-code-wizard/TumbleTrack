class Handler:
	"""
	confirm_test_message+3+hello+4.5+!thermometer
	"""
	def __init__(self):
		self._commands = {}
		self._objects = {}
		self._space_char = "+"
		self._obj_char = "!"

	def register_command(self, func):
		self._commands[func.__name__] = func
		return True

	def register_object(self, obj, name):
		self._objects[name] = obj
		return True

	def register_object_dict(self, object_dict):
		self._objects = {**self._objects, **object_dict}
		return True

	def _parse_arg_type(self, arg):
		if arg[0] == self._obj_char:
			if arg[1:] in self._objects.keys():
				return self._objects[arg[1:]]
			else:
				raise NotImplementedError
		else:
			try:
				return int(arg)
			except ValueError:
				try:
					return float(arg)
				except ValueError:
					return arg

	def _parse_command(self, packet):
		parsed_command = packet.split(self._space_char)[0]
		if parsed_command in self._commands.keys():
			return self._commands[parsed_command]
		else:
			raise NotImplementedError

	def _parse_args(self, packet):
		parsed_args = packet.split(self._space_char)[1:]
		parsed_args_dict = []
		for arg in parsed_args:
			parsed_args_dict.append(self._parse_arg_type(arg))
		return parsed_args_dict

	def handle_packet(self, packet):
		command = self._parse_command(packet)
		args = self._parse_args(packet)
		return command(*args)

	def handle_internal(self, command, *args):
		command = self._parse_command(command)
		return command(*args)
