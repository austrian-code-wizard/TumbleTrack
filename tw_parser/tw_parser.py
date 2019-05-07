import serial
import asyncio
from dataclasses import dataclass, field
from queue import PriorityQueue, Queue, Empty
from threading import Thread
from time import sleep


@dataclass(order=True)
class PrioritizedItem:
	priority: int
	item: bytes = field(compare=False)


class Parser:
	def __init__(self, controller, port: str):
		self._controller = controller
		self._port = port
		self._baud = 9600
		self._data_in = Queue()
		self._data_out = PriorityQueue()
		self._serial_port = None
		self._loop = None
		self._is_running = False
		self._batch_size = 32
		self._start_flag = "<"
		self._end_flag = ">"
		self._message_id_bytes = 4
		self._packet_id_bytes = 3
		self._message_id_count = 0
		self._packet_id_count = 0
		self._start_message = "start"
		self._pass_message = "pass"
		self._thread = None

	@staticmethod
	def chunkstring(string: str, length: int) -> str:
		return (string[0 + i:length + i] for i in range(0, len(string), length))

	@staticmethod
	def int_to_bytes(number: int, length):
		return number.to_bytes(length=length, byteorder="big")

	def _receive(self) -> str:
		reading = False
		message = ""
		while True:
			new_char = (self._serial_port.read(1)).decode()
			if new_char == self._start_flag and reading is False:
				reading = True
			elif new_char == self._end_flag and reading is True:
				return message
			elif reading is True:
				message += new_char

	def _prepare_for_sending(self, packet: bytes) -> bytes:
		return self._start_flag.encode() + packet + self._end_flag.encode()

	def _remove_flags(self, packet: str) -> str or bool:
		if packet[0] != self._start_flag or packet[-1] != self._end_flag:
			return False
		else:
			return packet[1:-1]

	def _next_message_id(self) -> bytes:
		self._message_id_count += 1
		return Parser.int_to_bytes(self._message_id_count, self._message_id_bytes)

	def _next_packet_id(self) -> bytes:
		self._packet_id_count += 1
		return Parser.int_to_bytes(self._packet_id_count, self._packet_id_bytes)

	def send_dataset(self, dataset: str, priority: int) -> bool:
		data_set_id = self._next_message_id()
		content_count = 256 - 2 - self._message_id_bytes - self._packet_id_bytes
		for packet in Parser.chunkstring(dataset, content_count):
			ready_packet = self._prepare_for_sending(data_set_id + self._next_packet_id() + packet.encode())
			self._data_out.put(PrioritizedItem(priority=priority, item=ready_packet))
		self._packet_id_count = 0
		return True

	async def _process_incoming_data(self) -> bool:
		async for data in self._get_next_incoming_packet():
			if data is not False:
				self._controller.handle_command(data)
			else:
				await asyncio.sleep(2)
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
		start = False
		print("trying to start") # TODO: logger
		while start is False:
			self._serial_port.write(self._prepare_for_sending(self._start_message.encode()))
			received_start_message = self._receive()
			if received_start_message == self._start_message:
				start = True
				print("starting") # TODO: logger
		async for next_packet in self._get_next_outgoing_packet():
			if next_packet is not False:
				self._serial_port.write(next_packet.item)
			else:
				await asyncio.sleep(2)
				self._serial_port.write(self._prepare_for_sending(self._pass_message.encode()))
			try:
				received_message = self._receive()
				print(received_message)
			except Exception as e:
				print(e)
			if received_message != self._pass_message:
				self._data_in.put(received_message)
			if self._is_running is False:
				return True

	def connect_to_arduino(self) -> bool:
		try:
			self._serial_port = serial.Serial(port=self._port, baudrate=self._baud)
			return True
		except Exception as e:
			print(e)  # TODO: add logger
			self._serial_port = None
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
		if self._serial_port is None:
			return False
		self._thread = Thread(target=self._run, args=())
		self._thread.start()

	def stop(self) -> bool:
		self._is_running = False
		sleep(1)
		return True



