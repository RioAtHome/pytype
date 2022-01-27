import urwid
import logging
from widgets.timer import Timer

TEXT = "Hello this is an example text to type out."
logging.basicConfig(filename='example.log')

# Maybe we need to lift things to main? or shorten name
# Stay on one naming convention please!!
class Typing:
	def __init__(self, eventManager):
		self.firstentry = True
		self.eventManager = eventManager
		self.timerComponent = Timer(eventManager=self.eventManager)
		self.timerWidget = self.timerComponent.timeView

		self.typeText = urwid.Text(TEXT)
		self.cursorPlaceholder = urwid.Edit()

		self.backButton = urwid.Button("Back")
		self.resetButton = urwid.Button("Reset")
		self.quitButton = urwid.Button("Quit")
		self.newButton = urwid.Button("New Test")
		urwid.connect_signal(self.backButton, 'click', self.back_menu, user_args=[])
		urwid.connect_signal(self.quitButton, 'click', self.exit, user_args=[])
		urwid.connect_signal(self.newButton, 'click', self.new_test, user_args=[])
		urwid.connect_signal(self.cursorPlaceholder, 'change', self.startTest, user_args=[])

		self.buttonsList = [self.backButton, self.resetButton, self.newButton, self.quitButton]
		self.colButtoms = urwid.Columns(self.buttonsList)
		
		self.componentBody = [self.timerWidget, self.typeText,self.cursorPlaceholder , self.colButtoms]
		self.componentPile = urwid.Pile(self.componentBody)
		
	def startTest(self, *user_args):
		if self.firstentry == True:
			self.firstentry = False
			self.Timertask = self.eventManager.create_task(self.timerComponent.startTimer())
			urwid.connect_signal(self.resetButton, 'click', self.reset_test, user_args=[self.Timertask])
			self.eventManager.create_task(self.timer_done())
		else:
			pass

	def back_menu(self, *user_args):
		pass

	async def timer_done(self, *user_args):
		await self.Timertask


	def reset_test(self, *user_args):
		self.timerComponent.resetTimer(task=user_args[0])
		self.cursorPlaceholder.edit_text = ''
		self.firstentry = True

	def new_test(self, *user_args):
		pass

	def exit(self, *user_args):
		raise urwid.ExitMainLoop()

		

