from twHandler.handlerMethods import handler


class TWException(Exception):
	pass


class SensorConnectionException(TWException):
	def __init__(self, sensor):
		pass

class SensorInaccuracyException(TWException):
	def __init__(self,sensor):
		pass