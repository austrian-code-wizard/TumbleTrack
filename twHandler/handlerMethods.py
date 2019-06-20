from twHandler.handler import Handler

handler = Handler()


@handler.register_command
def set_value(object, attribute_name, value):
	if attribute_name[0] == "_":
		raise ValueError("Setting of private attributes not allowed")
	setattr(object, attribute_name, value)
	return True


@handler.register_command
def set_private_value(object, attribute_name, value):
	setattr(object, attribute_name, value)
	return True


@handler.register_command
def confirm_test_message():
	print("I received a test command!")


@handler.register_command
def get_single_measurement(obj):
	if hasattr(obj, "get_single_measurement"):
		return obj.get_single_measurement()
	else:
		return None # TODO: Raise error

