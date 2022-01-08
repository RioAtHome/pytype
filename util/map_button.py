import urwid
from widgets.options import options
from widgets.typing import typing as start
from widgets.records import records


def quit(*args):
	raise urwid.ExitMainLoop()

Map_button = {
	"Start":start,
	"Options":options,
	"Previous Records":records,
	"Quit": quit	
}
