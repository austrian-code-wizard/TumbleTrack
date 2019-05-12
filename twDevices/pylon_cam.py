from twABCs.sensor import Sensor


class PylonCam(Sensor):

	def __init__(self):
		pass

	def check(self) -> bool:
		pass

	def _measure_value(self):
		pass

	def get_single_measurement(self):
		pass

	async def _measure_continuously(self):
		pass

	def start(self, loop):
		pass

	def stop(self) -> bool:
		pass