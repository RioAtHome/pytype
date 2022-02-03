import urwid
import logging
import asyncio
from widgets.typing import Typing
from widgets.timer import Timer
from widgets.results import Results
from util.textgenerator import get_text

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

palette = [('netural', '', ''),
		   ('wronginput', 'dark red',''),
		   ('rightinput', 'dark green', '')
]

class Main:
	def __init__(self):
		self.event_manager = asyncio.get_event_loop()
		self.timer_componenet = Timer(timer=15)
		self.typing_component = Typing(get_text())
		self.exit_button = urwid.Button('Quit')
		self.reset_test = urwid.Button('Reset')
		self.new_test = urwid.Button('New Test')

		self.buttons_col = urwid.Columns([self.exit_button, self.reset_test, self.new_test])


		self.main_pile = urwid.Pile([self.timer_componenet, self.typing_component, self.buttons_col])

		self.padding = urwid.Padding(self.main_pile, left=2, right=2)
		self.filler = urwid.Filler(self.padding)
		self.async_loop = urwid.AsyncioEventLoop(loop=self.event_manager)
		self.urwid_loop = urwid.MainLoop(self.filler, palette, event_loop=self.async_loop)
		
		urwid.connect_signal(self.typing_component, 'change', self.type_checking)
		urwid.connect_signal(self.exit_button, 'click', self._exit)
		urwid.connect_signal(self.new_test, 'click', self._new_test)

	def type_checking(self, _, string_typed):
		typing_status = self.typing_component.check_input(string_typed)
		if(typing_status == True):
			urwid.connect_signal(self.reset_test, 'click', self._reset_test)
			self.timer_task = asyncio.create_task(self.timer_componenet.start_timer())
			self.event_manager.create_task(self.timer_done())

		elif(typing_status == False):
			self.timer_task.cancel()
			self.time = self.timer_componenet.cancel_timer()


			self.buttons_col.widget_list = [self.exit_button]
			self.main_pile.widget_list = [Results(self.typing_component.get_results(),
									  self.time), self.buttons_col]


	async def timer_done(self):
		await self.timer_task

		self.timer_task.cancel()
		self.time = self.timer_componenet.cancel_timer()

		self.buttons_col.widget_list = [self.exit_button]
		self.main_pile.widget_list = [Results(self.typing_component.get_results(),
									  self.time), self.buttons_col]

	def _reset_test(self, *user_args):
		urwid.disconnect_signal(self.typing_component, 'change', self.type_checking)
		
		self.timer_task.cancel()
		self.timer_componenet.reset_timer()
		self.typing_component.reset_test()

		urwid.connect_signal(self.typing_component, 'change', self.type_checking)


	def _new_test(self, user_args):
		urwid.disconnect_signal(self.typing_component, 'change', self.type_checking)
		try:
			self.timer_task.cancel()
		except AttributeError:
			pass

		self.timer_componenet.reset_timer()
		self.typing_component.new_test(get_text())
		
		urwid.connect_signal(self.typing_component, 'change', self.type_checking)



	def _exit(self, *user_args):
		raise urwid.ExitMainLoop()


if __name__ == "__main__":
	Main().urwid_loop.run()