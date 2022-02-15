import logging
import asyncio
import urwid
from widgets.typing import Typing
from widgets.timer import Timer
from widgets.recordswidget import RecordsPile
from util.file_handling import read_file, write_file, create_file, FileNotFound
from util.calculate_util import calculate_acc, word_per_min
from widgets.boxbutton import BoxButton
from util.textgenerator import get_text
from datetime import date

logging.basicConfig(filename='example.log', encoding='utf-8',
                    level=logging.DEBUG)

PATH = "./user_records.json"

palette = [('netural', '', ''),
           ('wronginput', 'dark red', ''),
           ('rightinput', 'dark green', ''),
           ('highlight', 'black', 'dark green')]

# To do:
# [x] add the ability to change timer as user please
# [x] Style results more..
# [x] Reset and new test buttons work after completion
# [x] make default text if no connection is available
# [x] save user texts
# [] save user records
# [] add argparser so user can quickly enter his desired text/timer
# [] add theme palettes
# [] add colors to results precentages, ie 90+ green 70-80 green-ish... like that

# Bugs:
# If user didnt input anything, results will be 100%, we dont want that.

# event manager exceptions, text exception, timer exception


class AppWidget(urwid.Filler):
    # should only initalize the loop and main pile..
    # lets make every function more independently
    def __init__(self, text, timer, event_manager):
        self.timer_task = None
        self.event_manager = event_manager
        # setting up typing/timer widgets

        typer_widget = self.setup_typing_widget(text)
        timer_widget = self.setup_timer_widget(timer)

        # setting up button component
        exit_button = BoxButton('Quit', on_press=self.exit_)
        self.reset_test = BoxButton('Reset')
        self.new_test = BoxButton('New Test', on_press=self._new_test)
        previous_records = BoxButton('Previous Records', on_press=self.get_records)
        buttons_col = urwid.Columns([exit_button, self.reset_test, self.new_test, previous_records])

        self.container_buttons_col = urwid.LineBox(buttons_col)

        # setup main_pile correctly, where you can change upper widgets as you like, but buttons stay the same!
        # function that setups the mainpile
        self.main_pile = urwid.Pile([timer_widget, typer_widget, self.container_buttons_col])

        self.padding = urwid.Padding(self.main_pile, left=2, right=2)

        super().__init__(self.padding)

        urwid.connect_signal(self.typing_component, 'change', self.type_checking)

    def setup_timer_widget(self, timer):
        self.timer_componenet = Timer(timer=timer, align='center')
        container_timer = urwid.LineBox(self.timer_componenet)

        return container_timer

    def setup_typing_widget(self, text):
        self.typing_component = Typing(text)
        container_typing = urwid.LineBox(self.typing_component)

        return container_typing

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
        user_data = {
            "Word Per Min": word_per_min(results_array, time),
            "Accuracy": calculate_acc(results_array),
            "Timer": time,
            "Date": date.today().strftime("%d/%m/%Y")
        }
        write_file(path=PATH, key_value='Previous records', user_data=user_data)

    def exit_(self, *user_args):
        raise urwid.ExitMainLoop()

    def get_records(self, *args):
        try:
            state = read_file(PATH, key_value="Previous records")
        except FileNotFound:
            state = None
            create_file(PATH)

        self.main_pile.widget_list = [RecordsPile(state),  self.container_buttons_col]


if __name__ == "__main__":
    text = get_text()
    event_manager = asyncio.get_event_loop()
    app_widget = AppWidget(text=text, timer=20, event_manager=event_manager)
    async_loop = urwid.AsyncioEventLoop(loop=event_manager)
    urwid_loop = urwid.MainLoop(app_widget, palette, event_loop=async_loop)
    urwid_loop.run()
