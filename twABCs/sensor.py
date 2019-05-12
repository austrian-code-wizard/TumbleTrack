import abc


class Sensor(abc.ABC):

	@abc.abstractmethod
	def __init__(self):
		"""
		Set up attributes and connect to the device.
		"""
		pass

	@abc.abstractmethod
	def check(self) -> bool:
		"""
		Check if the sensor is connected and works.
		"""
		pass

	@abc.abstractmethod
	def _measure_value(self):
		"""
		Take a single measurement from the device and return it. One device might have several things that it measures.
		In that case, measure all the different things and return them as a list.
		"""
		pass

	@abc.abstractmethod
	def get_single_measurement(self):
		"""
		Take a single measurement and return it
		"""
		pass

	@abc.abstractmethod
	async def _measure_continuously(self):
		"""
		Continuously take measurements and send them to the sensor's controller.
		"""
		pass

	@abc.abstractmethod
	def start(self, loop):
		"""
		Start measuring continuously.
		"""
		pass

	@abc.abstractmethod
	def stop(self) -> bool:
		"""
		Stop measuring continuously.
		"""
		pass








