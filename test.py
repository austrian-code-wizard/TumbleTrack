import asyncio
from time import sleep

async def run():
	number = 0
	while number < 15:
		await asyncio.sleep(2)
		number += 1
		yield number

class Test:
	result = None

	async def sub(self):
		async for i in run():
			Test.result = i
			self.print_item(i)

	async def proc(self):
		while True:
			print("running")
			await asyncio.sleep(0.5)
			if Test.result is not None:
				print(Test.result)
				if Test.result == 14:
					return
				Test.result = None

	def print_item(self, item):
		print("not async")
		print(item)
		print("done not async")

loop = asyncio.get_event_loop()
t = Test()
loop.create_task(t.sub())
loop.create_task(t.proc())
loop.run_forever()
loop.close()