import urwid
import logging
from widgets.timer import Timer
from widgets.results import Results
from util.textgenerator import get_text

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

# Stay on one naming convention please!!
# Ugly code, too many if/else statement... think of a way around that my man

class Typing:
	def __init__(self, event_manager, urwid_loop, parent_widget):
		self.urwid_loop = urwid_loop
		self.parent_widget = parent_widget

		self.text = get_text(3)
		self.sentence_array = list(self.text)
		self.checking_array = []

		self.previous_state = []
		self.cursor_pointer = 0

		self.event_manager = event_manager
		self.timer_component = Timer()
		self.timer_widget = self.timer_component.time_view

		self.text_to_type = urwid.Text(('netural', self.text))
		self.cursor_placer = urwid.Edit()


		self.reset_button = urwid.Button("Reset")
		self.quit_button = urwid.Button("Quit")
		self.new_test_button = urwid.Button("New Test")
		self.set_timer_edit = urwid.IntEdit("Timer:")

		urwid.connect_signal(self.quit_button, 'click', self.exit)
		urwid.connect_signal(self.new_test_button, 'click', self.new_test)
		urwid.connect_signal(self.reset_button, 'click', self.reset_test)
		urwid.connect_signal(self.cursor_placer, 'change', self.start_test)

		self.list_buttons = [self.reset_button, self.new_test_button, self.quit_button]
		self.columns_buttons = urwid.Columns(self.list_buttons)
		self.timer_column = urwid.Columns([self.set_timer_edit])
		
		self.component_body = [self.timer_widget, self.text_to_type, self.cursor_placer , self.columns_buttons, self.timer_column]
		self.component_pile = urwid.Pile(self.component_body)
		


	def start_test(self, *user_args):
		if self.cursor_pointer != len(self.sentence_array) - 1:
			if self.cursor_pointer == 0:
				if self.set_timer_edit.value() != 0:
					logging.info('HUH?')
					self.timer_component.set_timer(timer=self.set_timer_edit.value())

				self.keypress = user_args[1]

				self.timer_task = self.event_manager.create_task(self.timer_component.start_timer())
				self.event_manager.create_task(self.timer_done())

				if self.keypress == self.sentence_array[self.cursor_pointer]:
					self.previous_state.append(('rightinput', self.text[self.cursor_pointer:self.cursor_pointer+1]))
					self.checking_array.append(True)
					
					self.text_to_type.set_text([ self.previous_state,
											('netural', self.text[self.cursor_pointer+1:])])
					
					self.urwid_loop.screen.clear()

				elif self.keypress != self.sentence_array[self.cursor_pointer]:
					self.previous_state.append(('wronginput', self.text[self.cursor_pointer:self.cursor_pointer+1]))
					self.checking_array.append(False)
					self.text_to_type.set_text([self.previous_state,
											('netural', self.text[self.cursor_pointer+1:])])
				self.cursor_pointer +=1

			else:
				if len(user_args[1]) >= self.cursor_pointer:

					self.keypress = user_args[1][self.cursor_pointer]

					if self.keypress == self.sentence_array[self.cursor_pointer]:
						self.checking_array.append(True)
						self.previous_state.append(('rightinput', self.text[self.cursor_pointer:self.cursor_pointer+1]))
						
						self.text_to_type.set_text([ self.previous_state,
												('netural', self.text[self.cursor_pointer+1:])])
						
						self.urwid_loop.screen.clear()

					else:
						self.previous_state.append(('wronginput', self.text[self.cursor_pointer:self.cursor_pointer+1]))
						self.checking_array.append(False)
						self.text_to_type.set_text([ self.previous_state,
												('netural', self.text[self.cursor_pointer+1:])])
						
						self.urwid_loop.screen.clear()

					self.cursor_pointer +=1
				else:
					self.previous_state.pop()
					self.cursor_pointer -=1
					self.text_to_type.set_text([ self.previous_state,
												('netural', self.text[self.cursor_pointer:])])

					self.urwid_loop.screen.clear()

		else:
			time = self.timer_component.cancel_timer(task=self.timer_task)
			self.results = Results(checking_array=self.checking_array,
								   time=time
									   )
			self.parent_widget.widget_list = [self.results.pile()]


	async def timer_done(self, *user_args):
		await self.timer_task
		time = self.timer_component.cancel_timer(task=self.timer_task)
		self.results = Results(checking_array=self.checking_array,
								   time=time
									   )
		self.parent_widget.widget_list = [self.results.pile()]

	def reset_test(self, *user_args):
		if self.cursor_pointer != 0:
			self.timer_component.reset_timer(task=self.timer_task)
			self.cursor_placer.set_edit_text('')
			
			self.cursor_pointer = 0
			self.previous_state = []
			self.checking_array = []
		self.text_to_type.set_text(('netural', self.text))
			
		self.urwid_loop.screen.clear()	
			
	def new_test(self, *user_args):
		self.text = get_text(3)
		self.sentence_array = list(self.text)
		self.reset_test()
		

	def exit(self, *user_args):
		raise urwid.ExitMainLoop()

		

