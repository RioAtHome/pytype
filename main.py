import urwid
from widgets.menu import menu

# if elment in menu list doesnt have a function, return error

menu_item=['Start', 'Options', 'Previous Records', 'Quit']

def _main():
	list_menu = urwid.ListBox(menu(menu_item))
	main = urwid.Padding(list_menu, left=2, right=2)
	top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    align='center', width=('relative', 60),
    valign='middle', height=('relative', 60),
    min_width=20, min_height=9)
    
	_loop = urwid.MainLoop(top)
	return _loop

if __name__ == "__main__":
	_main().run()
