import urwid


class BoxButton(urwid.WidgetWrap):
    def __init__(self, label, on_press=None,
                 user_data=None, when_focused='highlight'):
        self.button = urwid.Button(label, on_press=on_press,
                                   user_data=user_data)
        attrmap_container = urwid.AttrMap(self.button, '', when_focused)
        linebox_container = urwid.LineBox(attrmap_container)
        padding_container = urwid.Padding(linebox_container, left=2, right=2)

        super().__init__(padding_container)

    def set_signal(self, on_press, user_data=None):
        urwid.connect_signal(self.button, 'click', on_press,
                             user_args=user_data)

    def disable_signal(self, on_press, user_data=None):
        urwid.disconnect_signal(self.button, 'click', on_press,
                                user_args=user_data)
