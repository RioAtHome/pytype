import urwid
import logging
import asyncio

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

class Timer:
	def __init__(self, timer=30):
		self.time_count = timer
		self.time_view = urwid.Text(f'Timer:{self.time_count}')
	
	def set_timer(self, timer):
		self.time_count = timer
		self.time_view.set_text(f'Timer:{self.time_count}')
			
	async def start_timer(self):
		self.timer = self.time_count
		while True:
			if self.timer == 0:
				return

			self.timer -= 1
			self.time_view.set_text(f'Timer:{self.timer}')
			await asyncio.sleep(1)		

	def reset_timer(self, task):
		task.cancel()
		self.time_view.set_text(f'Timer:{self.time_count}')

	def cancel_timer(self, task):
		task.cancel()
		return (self.time_count - self.timer)