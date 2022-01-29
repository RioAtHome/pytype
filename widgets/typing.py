import urwid
import logging
from widgets.timer import Timer
from widgets.results import Results

TEXT = "Hello"
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

# Maybe we need to lift things to main? or shorten name
# Stay on one naming convention please!!
# Ugly code, too many if/else statement... think of a way around that my man

class Typing:
	def __init__(self, eventManager, oldbody, parent, urwidloop):
		self.oldbody = oldbody
		self.parent = parent
		self.urwidloop = urwidloop

		self.sentenceArr = list(TEXT)
		self.checkArr = []

		self.previousState = []
		self.indexpointer = 0

		self.eventManager = eventManager
		self.timerComponent = Timer(eventManager=self.eventManager)
		self.timerWidget = self.timerComponent.timeView

		self.typeText = urwid.Text(('netural', TEXT))
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
		if self.indexpointer != len(self.sentenceArr):
			if self.indexpointer == 0:
				self.keyEntry = user_args[1]

				self.Timertask = self.eventManager.create_task(self.timerComponent.startTimer())
				urwid.connect_signal(self.resetButton, 'click', self.reset_test, user_args=[])
				self.eventManager.create_task(self.timer_done())

				if self.keyEntry == self.sentenceArr[self.indexpointer]:
					self.previousState.append(('rightinput', TEXT[self.indexpointer:self.indexpointer+1]))
					self.checkArr.append(True)
					
					self.typeText.set_text([ self.previousState,
											('netural', TEXT[self.indexpointer+1:])])
					
					self.urwidloop.screen.clear()

				elif self.keyEntry != self.sentenceArr[self.indexpointer]:
					self.previousState.append(('wronginput', TEXT[self.indexpointer:self.indexpointer+1]))
					self.checkArr.append(False)
					self.typeText.set_text([self.previousState,
											('netural', TEXT[self.indexpointer+1:])])
				self.indexpointer +=1

			else:
				if len(user_args[1]) >= self.indexpointer:

					self.keyEntry = user_args[1][self.indexpointer]

					if self.keyEntry == self.sentenceArr[self.indexpointer]:
						self.checkArr.append(True)
						self.previousState.append(('rightinput', TEXT[self.indexpointer:self.indexpointer+1]))
						
						self.typeText.set_text([ self.previousState,
												('netural', TEXT[self.indexpointer+1:])])
						
						self.urwidloop.screen.clear()

					else:
						self.previousState.append(('wronginput', TEXT[self.indexpointer:self.indexpointer+1]))
						self.checkArr.append(False)
						self.typeText.set_text([ self.previousState,
												('netural', TEXT[self.indexpointer+1:])])
						
						self.urwidloop.screen.clear()

					self.indexpointer +=1
				else:
					self.previousState.pop()
					self.indexpointer -=1
					self.typeText.set_text([ self.previousState,
												('netural', TEXT[self.indexpointer:])])

					self.urwidloop.screen.clear()

		else:
			self.timerComponent.cancel_timer(task=self.Timertask)
			self.results = Results(eventManager=self.eventManager,
									   oldbody=self.componentBody,
									   parent=self.parent,
									   urwidloop=self.urwidloop,
									   sentence=self.sentenceArr,
									   checkarr=self.checkArr
									   )
			self.parent.widget_list = self.results.pile


	def back_menu(self, *user_args):
		self.parent.widget_list = [urwid.Pile(self.oldbody)]

	async def timer_done(self, *user_args):
		await self.Timertask




	def reset_test(self, *user_args):
		# BUG!!! 
		# after two resets, app freezes.
		# Asyncio task is the suspect.....
		# i believe timer_done is waiting for the first task...

		self.timerComponent.resetTimer(task=self.Timertask)
		self.cursorPlaceholder.set_edit_text('')
		self.indexpointer = 0
		self.previousState = []
		self.typeText.set_text(('netural', TEXT))
		self.urwidloop.screen.clear()

	def new_test(self, *user_args):
		pass

	def exit(self, *user_args):
		raise urwid.ExitMainLoop()

		

