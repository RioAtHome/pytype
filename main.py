import urwid
import logging
import asyncio
from widgets.typing import Typing
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

palette = [('netural', '', ''),
		   ('wronginput', 'dark red',''),
		   ('rightinput', 'dark green', '')
]

class Main:
	def __init__(self):
		self.eventManager = asyncio.get_event_loop()
		self.body = [urwid.Text('')]
		self.mainPile = urwid.Pile(self.body)
		self.pad = urwid.Padding(self.mainPile, left=2, right=2)
		self.fill = urwid.Filler(self.pad)

		self.asyncloop = urwid.AsyncioEventLoop(loop=self.eventManager)
		self.urwidloop = urwid.MainLoop(self.fill, palette, event_loop=self.asyncloop)
		
		self.typingComponent = [Typing(eventManager=self.eventManager,
									   urwidloop=self.urwidloop,
									   parent=self.mainPile).componentPile]
		
		self.mainPile.widget_list = self.typingComponent

		self.urwidloop.run()
if __name__ == "__main__":
	Main()