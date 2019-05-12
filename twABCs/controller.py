import abc


class Controller(abc.ABC):

	@abc.abstractmethod
	def __init__(self):
		"""Set up attributes and create data_out_queue"""
		pass

	@abc.abstractmethod
	def register_sensor(self, sensor, name) -> bool:
		"""Register a sensor in the sensor dict"""
		pass

	@abc.abstractmethod
	def receive_data(self, data, device_code) -> bool:
		"""Put the data packet in the data_out queue"""
		pass

	@abc.abstractmethod
	def check_devices(self) -> bool:
		"""Check if all sensors connected are connected and work"""
		pass

	@abc.abstractmethod
	async def _process_outgoing_data(self) -> bool:
		"""Continuously get the new data packets from the data_out queue and send it to the parser"""
		pass

	@abc.abstractmethod
	async def _get_next_outgoing_packet(self) -> str or bool:
		"""Async generator that yields the next packet in the data_out queue or returns False if it is empty"""
		pass

	@abc.abstractmethod
	def _run(self) -> bool:
		"""Start all the connected sensors and run the loop"""
		pass

	@abc.abstractmethod
	def run(self) -> bool:
		"""Start the controller and its connected devices. Typically within a new thread"""
		pass

	@abc.abstractmethod
	def stop(self) -> bool:
		"""Stop the controller and all the connected sensors"""
		pass
