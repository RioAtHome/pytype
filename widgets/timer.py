import urwid
import logging
import asyncio

# Maybe lift task into task, single responsibility and all

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
class Timer:
	def __init__(self, eventManager,timer=10):
		self.timeCount = timer
		self.eventManager = eventManager
		self.timeView = urwid.Text(f'Timer:{self.timeCount}')
	
	async def startTimer(self, stop=False):
		timer = self.timeCount
		while True:
			if timer == 0:
				return

			timer -= 1
			self.timeView.set_text(f'Timer:{timer}')
			await asyncio.sleep(1)		

	def resetTimer(self, task):
		task.cancel()
		self.timeCount = 15
		self.timeView.set_text(f'Timer:{self.timeCount}')