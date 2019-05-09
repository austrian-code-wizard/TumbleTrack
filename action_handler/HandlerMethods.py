from action_handler.Handler import Handler

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
