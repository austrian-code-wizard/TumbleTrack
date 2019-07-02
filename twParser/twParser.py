import asyncio
from dataclasses import dataclass, field
from queue import PriorityQueue, Queue, Empty
from threading import Thread
from time import sleep
from math import ceil
import struct
from twDevices.arduinoSerial import ArduinoSerial
from twDevices.testSerial import TestSerial


@dataclass(order=True)
class PrioritizedItem:
	priority: int
	item: bytes = field(compare=False)


class Parser:
	def __init__(self, handler):
		self._controller = handler
		self._data_in = Queue()
		self._data_out = PriorityQueue()
		self._loop = None
		self._is_running = False
		self._batch_size = 32
		self._packet_size = 256
		self._start_flag = "<"
		self._end_flag = ">"
		self._message_id_bytes = 4
		self._packet_id_bytes = 2
		self._dtype_bytes = 1
		self._sensor_id_bytes = 2
		self._message_id_count = 0
		self._packet_id_count = 0
		self._start_message = "start"
		self._pass_message = "pass"
		#self._transceiverDevice = ArduinoSerial(self._start_flag, self._end_flag)
		self._transceiverDevice = TestSerial(self._start_flag, self._end_flag)
		self._thread = None

	@staticmethod
	def chunkstring(string: bytes, length: int) -> iter:
		return (string[0 + i:length + i] for i in range(0, len(string), length))

	@staticmethod
	def number_of_packets(packet: bytes, length: int) -> bytes:
		value = ceil(len(packet)/length)
		return Parser.ushort_to_bytes(value)

	@staticmethod
	def ushort_to_bytes(number: int) -> bytes:
		return struct.pack(">H", number)

	@staticmethod
	def uint_to_bytes(number: int) -> bytes:
		return struct.pack(">I", number)

	@staticmethod
	def double_to_bytes(number: float) -> bytes:
		return struct.pack(">d", number)

	@staticmethod
	def string_to_bytes(string: str) -> bytes:
		return string.encode()

	@staticmethod
	def char_to_bytes(char: str) -> bytes:
		return char.encode()

	@staticmethod
	def long_long_to_bytes(long: int) -> bytes:
		return struct.pack(">q", long)

	def _prepare_for_sending(self, packet: bytes) -> bytes:
		return Parser.char_to_bytes(self._start_flag) + packet + Parser.char_to_bytes(self._end_flag)

	def _next_message_id(self) -> bytes:
		self._message_id_count += 1
		return Parser.uint_to_bytes(self._message_id_count)

	def _next_packet_id(self) -> bytes:
		self._packet_id_count += 1
		return Parser.ushort_to_bytes(self._packet_id_count)

	def send_dataset(self, dataset: str, sensor_id: str, priority: int) -> bool:
		"""packet layout: start_flag(1) + message_id(4) + packet_id(3) + packet_number(3) + sensor_id(2) + dtype(1) +
		data + end_flag(1)"""
		data_set_id = self._next_message_id()
		assert len(sensor_id) == 2
		sensor_id = Parser.string_to_bytes(sensor_id)
		content_count = self._packet_size - self._message_id_bytes - self._packet_id_bytes - self._dtype_bytes \
						- self._sensor_id_bytes - self._packet_id_bytes
		if isinstance(dataset, int):
			dtype = Parser.char_to_bytes("I")
			dataset = Parser.long_long_to_bytes(dataset)
		elif isinstance(dataset, float):
			dtype = Parser.char_to_bytes("d")
			dataset = Parser.double_to_bytes(dataset)
		elif isinstance(dataset, bytes):
			dtype = Parser.char_to_bytes("b")
		else:
			dtype = Parser.char_to_bytes("s")
			dataset = Parser.string_to_bytes(str(dataset))
		number_of_packets = Parser.number_of_packets(dataset, content_count)
		for packet in Parser.chunkstring(dataset, content_count):
			ready_packet = self._prepare_for_sending(data_set_id + self._next_packet_id() + number_of_packets + dtype +
													 sensor_id + packet)
			self._data_out.put(PrioritizedItem(priority=priority, item=ready_packet))
		self._packet_id_count = 0
		return True

	async def _process_incoming_data(self) -> bool:
		async for data in self._get_next_incoming_packet():
			if data is not False:
				result = self._controller.handle_packet(data)
				self.send_dataset(result, "H1", 10)
			else:
				await asyncio.sleep(0.1)
			if self._is_running is False:
				return True

	async def _get_next_outgoing_packet(self) -> PrioritizedItem or bool:
		while self._is_running is True:
			try:
				yield self._data_out.get(timeout=False)
			except Empty:
				yield False

	async def _get_next_incoming_packet(self) -> str or bool:
		while self._is_running is True:
			try:
				yield self._data_in.get(timeout=False)
			except Empty:
				yield False

	async def _run_serial_communication(self) -> bool:
		# TODO: run calls to transceiverDevice in async executor to make them awaitable
		start = False
		print("trying to start")  # TODO: logger
		if self._transceiverDevice is None:
			raise ValueError("No transceiver device initialized")
		while start is False:
			self._transceiverDevice.write(self._prepare_for_sending(self._start_message.encode()))
			received_start_message = self._transceiverDevice.receive()
			if received_start_message == self._start_message:
				start = True
				print("starting")  # TODO: logger
		async for next_packet in self._get_next_outgoing_packet():
			if next_packet is not False:
				self._transceiverDevice.write(next_packet.item)
			else:
				await asyncio.sleep(1)
				self._transceiverDevice.write(self._prepare_for_sending(self._pass_message.encode()))
			try:
				received_message = self._transceiverDevice.receive()
			except Exception as e:
				print(e)
				received_message = None
				# TODO: handle properly
			if received_message != self._pass_message:
				self._data_in.put(received_message)
			if self._is_running is False:
				return True

	def connect(self, port=None) -> bool:
		try:
			return self._transceiverDevice.connect(port=port)
		except Exception as e:
			print(e)  # TODO: add logger
			self._transceiverDevice = None
			return False

	async def _send_test_message(self):
		while True:
			self.send_dataset("hi", 1)
			await asyncio.sleep(1)

	def _run(self) -> bool:
		self._is_running = True
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		loop.create_task(self._process_incoming_data())
		loop.create_task(self._run_serial_communication())
		self._loop = loop
		loop.run_forever()
		return True

	def run(self) -> bool:
		if self._transceiverDevice is None:
			return False
		self._thread = Thread(target=self._run, args=())
		self._thread.start()
		return True

	def stop(self) -> bool:
		self._is_running = False
		sleep(0.5)
		self._loop.call_soon_threadsafe(self._loop.stop)
		self._thread.join()
		self._thread = None
		return True



