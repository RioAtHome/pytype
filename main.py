import logging
import asyncio
import urwid
from widgets.typing import Typing
from widgets.timer import Timer
from util.calculate_util import calculate_acc, word_per_min
from widgets.boxbutton import BoxButton
from util.textgenerator import get_text

logging.basicConfig(filename='example.log', encoding='utf-8',
                    level=logging.DEBUG)

palette = [('netural', '', ''),
           ('wronginput', 'dark red', ''),
           ('rightinput', 'dark green', ''),
           ('highlight', 'black', 'dark green')]

# To do:
# [x] add the ability to change timer as user please
# [x] Style results more..
# [x] Reset and new test buttons work after completion
# [x] make default text if no connection is available
# [] save user texts
# [] save user records
# [] add theme palettes
# [] add colors to results precentages, ie 90+ green 70-80 green-ish... like that

# Bugs:
# If user didnt input anything, results will be 100%, we dont want that.


class Main:
    def __init__(self, text, timer):
        self.timer_task = None
        self.event_manager = asyncio.get_event_loop()

        self.settup_widgets = self.setup_widget(text=text, timer=timer)
        self.exit_button = BoxButton('Quit', on_press=self.exit_)
        self.reset_test = BoxButton('Reset')
        self.new_test = BoxButton('New Test', on_press=self._new_test)

        self.buttons_col = urwid.Columns([self.exit_button, self.reset_test,
                                          self.new_test])
        self.container_buttons_col = urwid.LineBox(self.buttons_col)

        self.settup_widgets.append(self.container_buttons_col)
        self.main_pile = urwid.Pile(self.settup_widgets)

        self.padding = urwid.Padding(self.main_pile, left=2, right=2)
        self.filler = urwid.Filler(self.padding)

        self.async_loop = urwid.AsyncioEventLoop(loop=self.event_manager)
        self.urwid_loop = urwid.MainLoop(self.filler, palette,
                                         event_loop=self.async_loop)

        urwid.connect_signal(self.typing_component, 'change', self.type_checking)

    def setup_widget(self, text, timer):
        self.timer_componenet = Timer(timer=timer, align='center')
        self.typing_component = Typing(text)
        self.container_typing = urwid.LineBox(self.typing_component)
        self.container_timer = urwid.LineBox(self.timer_componenet)

        return([self.container_timer, self.container_typing])

    def type_checking(self, _, string_typed):
        typing_status = self.typing_component.check_input(string_typed)
        if(typing_status is True):
            self.timer_componenet.set_timer()
            self.reset_test.set_signal(self._reset_test)

            try:
                self.timer_task = asyncio.create_task(self.timer_componenet.start_timer())
            except RuntimeError:
                self.timer_task = None

            self.event_manager.create_task(self.timer_done())

        elif(typing_status is False):
            self.test_done()

    async def timer_done(self):
        await self.timer_task
        self.test_done()

    def _reset_test(self, *user_args):
        if self.timer_task:
            self.timer_task.cancel()
        urwid.disconnect_signal(self.typing_component, 'change', self.type_checking)
        self.timer_componenet.reset_timer()
        self.typing_component.reset_test()

        self.main_pile.widget_list = [self.container_timer, self.container_typing,
                                      self.container_buttons_col]
        urwid.connect_signal(self.typing_component, 'change', self.type_checking)

    def _new_test(self, user_text=None, *args):
        # Avoiding the exception isnt the best way..
        user_text = get_text()
        urwid.disconnect_signal(self.typing_component, 'change', self.type_checking)

        if self.timer_task:
            self.timer_task.cancel()
        else:
            self.timer_componenet.reset_timer()
            self.typing_component.new_test(user_text)

        self.main_pile.widget_list = [self.container_timer, self.container_typing,
                                      self.container_buttons_col]

        urwid.connect_signal(self.typing_component, 'change', self.type_checking)

    def test_done(self):
        if self.timer_task:
            self.timer_task.cancel()

        time = self.timer_componenet.get_time_passed()
        results_array = self.typing_component.get_results()

        accuracy_text = urwid.Text(f'Accuracy:{calculate_acc(results_array)}%', align='center')
        word_per_min_text = urwid.Text(f'Typing Speed:{word_per_min(results_array, time)}/wpm', align='center')
        accuracy_container = urwid.LineBox(accuracy_text)
        word_per_min_container = urwid.LineBox(word_per_min_text)
        results_col = urwid.Columns([accuracy_container, word_per_min_container], dividechars=2)

        self.results_widget = urwid.Padding(results_col, left=2, right=2)
        self.container_results = urwid.LineBox(self.results_widget)

        self.timer_task = None
        self.main_pile.widget_list = [self.container_results,
                                      self.container_buttons_col]

    def exit_(self, *user_args):
        raise urwid.ExitMainLoop()


if __name__ == "__main__":
    text = get_text()

    Main(text=text, timer=20).urwid_loop.run()
