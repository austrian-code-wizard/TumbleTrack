from queue import Queue, Empty
from threading import Thread
from twABCs.controller import Controller
from time import sleep
import asyncio


class Atmos(Controller):
	def __init__(self, handler, parser):
		super().__init__()
		self._handler = handler
		self._parser = parser
		self._devices = {}
		self._data_out = Queue()
		self._is_running = False
		self._active = False
		self._standard_priority = 1
		self._loop = None
		self._thread = None

	@staticmethod
	def _wrap_data(data, device_code):
		return device_code + data + device_code

	def register_sensor(self, sensor, name):
		self._devices[name] = sensor
		self._handler.register_object(sensor, name)
		return True

	def receive_data(self, data, device_code):
		packet = Atmos._wrap_data(data, device_code)
		self._data_out.put(packet)
		return True

	def check_devices(self):
		all_clear = True
		for device in self._devices.keys():
			if not self._devices[device].check():
				all_clear = False
		return all_clear

	async def _process_outgoing_data(self) -> bool:
		async for data in self._get_next_outgoing_packet():
			if data is not False:
				self._parser.send_dataset(data, self._standard_priority)
			else:
				await asyncio.sleep(0.1)
			if self._is_running is False:
				return True

	async def _get_next_outgoing_packet(self) -> str or bool:
		while self._is_running is True:
			try:
				yield self._data_out.get(timeout=False)
			except Empty:
				yield False

	def _run(self) -> bool:
		self._is_running = True
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		loop.create_task(self._process_outgoing_data())
		for device in self._devices.keys():
			self._devices[device].start(loop)
		self._loop = loop
		loop.run_forever()
		return True

	def run(self) -> bool:
		self._thread = Thread(target=self._run, args=())
		self._thread.start()
		return True

	def stop(self) -> bool:
		self._is_running = False
		for device in self._devices.keys():
			self._devices[device].stop()
		sleep(1)
		return True
