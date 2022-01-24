import urwid
import logging
from widgets.typing import Typing

MENU_ITEMS = ['Start', 'Options', 'Previous Records', 'Quit']
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

class Main:
	def __init__(self, childrenWidgets):
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
		self.walker = urwid.SimpleFocusListWalker(self.body, wrap_around=True)
		
		self.mainPile = urwid.Pile(self.body)
		self.pad = urwid.Padding(self.mainPile, left=2, right=2)
		self.fill = urwid.Filler(self.pad)

	def start(self, *user_args):
		self.typingComponent = [Typing()]
		self.mainPile.widget_list = self.typingComponent


	def options(self, *user_args):
		pass

	def records(self, *user_args):
		pass

	def _quit(self, *user_args):
		raise urwid.ExitMainLoop()

if __name__ == "__main__":
	wid = Main(MENU_ITEMS)
	urwid.MainLoop(wid.fill).run()