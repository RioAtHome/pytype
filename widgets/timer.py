import urwid
import logging
import asyncio

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

class Timer(urwid.Edit):
	def __init__ (self, timer=60, align='left'):
		self.time_count = timer
		super().__init__(caption='Timer:',edit_text='15', align=align)
	
	def set_timer(self, timer):
		self.time_count = timer
		super().set_edit_text(f'{self.time_count}')

			
	async def start_timer(self):
		self.timer = self.time_count
		while True:
			if self.timer == 0:
				return

			self.timer -= 1
			super().set_edit_text(f'{self.time_count}')
			await asyncio.sleep(1)		

	def reset_timer(self):
		super().set_edit_text(f'{self.time_count}')

	def cancel_timer(self):
		return (self.time_count - self.timer)

	def keypress(self, size, key):
		allowed_chars = ('up', 'down', 'right', 'left',
						 '0', '9', '8', '7', '6', '5',
						 '4', '3', '2', '1', 'backspace', 'enter')

		super().keypress(size, key)