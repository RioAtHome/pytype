import urwid
import logging
import asyncio
from widgets.typing import Typing

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

palette = [('netural', '', ''),
		   ('wronginput', 'dark red',''),
		   ('rightinput', 'dark green', '')
]

# Refactor Things to single responsibility Principle....
# loose coupling if you may, before writing unit tests.
# And, make some classes actual classes...
# make some functions return sth ffs
# change shit
# its all tightly coupled its a disgrace!!

class Main:
	def __init__(self):
		self.event_manager = asyncio.get_event_loop()
		self.body = [urwid.Text('')]
		self.main_pile = urwid.Pile(self.body)
		
		self.padding = urwid.Padding(self.main_pile, left=2, right=2)
		self.filler = urwid.Filler(self.padding)

		self.async_loop = urwid.AsyncioEventLoop(loop=self.event_manager)
		self.urwid_loop = urwid.MainLoop(self.filler, palette, event_loop=self.async_loop)
		
		self.typing_component = [Typing(event_manager=self.event_manager,
									   urwid_loop=self.urwid_loop,
									   parent_widget=self.main_pile).component_pile]
		
		self.main_pile.widget_list = self.typing_component

		self.urwid_loop.run()
if __name__ == "__main__":
	Main()