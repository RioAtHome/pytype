import urwid
import logging
import asyncio
from widgets.typing import Typing

MENU_ITEMS = ['Start', 'Options', 'Previous Records', 'Quit']

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

palette = [('netural', '', ''),
		   ('wronginput', 'dark red',''),
		   ('rightinput', 'dark green', '')
]

# cut it down, remove options and records, and put a timer to set on bottom...

class Main:
	def __init__(self, childrenWidgets=MENU_ITEMS):
		self.eventManager = asyncio.get_event_loop()
		
		self.functionMap = {
			"Start":self.start,
			"Options":self.options,
			"Previous Records":self.records,
			"Quit": self._quit	
		}

		self.body = [urwid.Divider(), urwid.Text('Options'), urwid.Divider()]
		for child in childrenWidgets:
			self.button = urwid.Button(child)
			try:
				urwid.connect_signal(self.button, 'click', self.functionMap[child], user_args=[])
			except KeyError:
					traceback.print_exc()
			self.body.append(urwid.AttrMap(self.button, None, focus_map='reversed'))
		
		self.mainPile = urwid.Pile(self.body)
		self.pad = urwid.Padding(self.mainPile, left=2, right=2)
		self.fill = urwid.Filler(self.pad)

		self.asyncloop = urwid.AsyncioEventLoop(loop=self.eventManager)
		self.urwidloop = urwid.MainLoop(self.fill, palette, event_loop=self.asyncloop)
		self.urwidloop.run()

	def start(self, *user_args):
		self.typingComponent = [Typing(eventManager=self.eventManager,
									   oldbody=self.body,
									   parent=self.mainPile,
									   urwidloop=self.urwidloop).componentPile]
		
		self.mainPile.widget_list = self.typingComponent


	def options(self, *user_args):
		pass

	def records(self, *user_args):
		pass

	def _quit(self, *user_args):
		raise urwid.ExitMainLoop()

if __name__ == "__main__":
	Main()