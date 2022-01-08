import urwid
import traceback
from util.map_button import Map_button



def menu(list_element):
	body = [urwid.Divider(), urwid.Text('Options'), urwid.Divider()]
	for element in list_element:
		button = urwid.Button(element)
		try:
			urwid.connect_signal(button, 'click', Map_button[element] , element)
		except KeyError:
				traceback.print_exc()
		body.append(urwid.AttrMap(button, None, focus_map='reversed'))

	return urwid.SimpleFocusListWalker(body)

