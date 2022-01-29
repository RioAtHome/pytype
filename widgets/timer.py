import urwid
import logging
import asyncio

# Maybe lift task into task, single responsibility and all

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
class Timer:
	def __init__(self, timer=30):
		self.timeCount = timer
		self.timeView = urwid.Text(f'Timer:{self.timeCount}')
	
	def set_timer(self, timer):
		self.timeCount = timer
		self.timeView.set_text(f'Timer:{self.timeCount}')
			
	async def startTimer(self):
		self.timer = self.timeCount
		while True:
			if self.timer == 0:
				return

			self.timer -= 1
			self.timeView.set_text(f'Timer:{self.timer}')
			await asyncio.sleep(1)		

	def resetTimer(self, task):
		task.cancel()
		self.timeView.set_text(f'Timer:{self.timeCount}')

	def cancel_timer(self, task):
		task.cancel()
		return (self.timeCount - self.timer)