import urwid
import logging
from widgets.timer import Timer
from widgets.results import Results
from util.textgenerator import get_text

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

# Stay on one naming convention please!!
# Ugly code, too many if/else statement... think of a way around that my man

class Typing:
	def __init__(self, eventManager, urwidloop, parent):
		self.urwidloop = urwidloop
		self.parent = parent

		self.text = get_text()
		self.sentenceArr = list(self.text)
		self.checkArr = []

		self.previousState = []
		self.indexpointer = 0

		self.eventManager = eventManager
		self.timerComponent = Timer()
		self.timerWidget = self.timerComponent.timeView

		self.typeText = urwid.Text(('netural', self.text))
		self.cursorPlaceholder = urwid.Edit()


		self.resetButton = urwid.Button("Reset")
		self.quitButton = urwid.Button("Quit")
		self.newButton = urwid.Button("New Test")
		self.setTimerEdit = urwid.IntEdit("Timer:")

		urwid.connect_signal(self.quitButton, 'click', self.exit)
		urwid.connect_signal(self.newButton, 'click', self.new_test)
		urwid.connect_signal(self.resetButton, 'click', self.reset_test)
		urwid.connect_signal(self.cursorPlaceholder, 'change', self.startTest)

		self.buttonsList = [self.resetButton, self.newButton, self.quitButton]
		self.colButtoms = urwid.Columns(self.buttonsList)
		self.timerCol = urwid.Columns([self.setTimerEdit])
		
		self.componentBody = [self.timerWidget, self.typeText, self.cursorPlaceholder , self.colButtoms, self.timerCol]
		self.componentPile = urwid.Pile(self.componentBody)
		
	def startTest(self, *user_args):
		if self.indexpointer != len(self.sentenceArr) - 1:
			if self.indexpointer == 0:
				if self.setTimerEdit.value() != 0:
					logging.info('HUH?')
					self.timerComponent.set_timer(timer=self.setTimerEdit.value())

				self.keyEntry = user_args[1]

				self.Timertask = self.eventManager.create_task(self.timerComponent.startTimer())
				self.eventManager.create_task(self.timer_done())

				if self.keyEntry == self.sentenceArr[self.indexpointer]:
					self.previousState.append(('rightinput', self.text[self.indexpointer:self.indexpointer+1]))
					self.checkArr.append(True)
					
					self.typeText.set_text([ self.previousState,
											('netural', self.text[self.indexpointer+1:])])
					
					self.urwidloop.screen.clear()

				elif self.keyEntry != self.sentenceArr[self.indexpointer]:
					self.previousState.append(('wronginput', self.text[self.indexpointer:self.indexpointer+1]))
					self.checkArr.append(False)
					self.typeText.set_text([self.previousState,
											('netural', self.text[self.indexpointer+1:])])
				self.indexpointer +=1

			else:
				if len(user_args[1]) >= self.indexpointer:

					self.keyEntry = user_args[1][self.indexpointer]

					if self.keyEntry == self.sentenceArr[self.indexpointer]:
						self.checkArr.append(True)
						self.previousState.append(('rightinput', self.text[self.indexpointer:self.indexpointer+1]))
						
						self.typeText.set_text([ self.previousState,
												('netural', self.text[self.indexpointer+1:])])
						
						self.urwidloop.screen.clear()

					else:
						self.previousState.append(('wronginput', self.text[self.indexpointer:self.indexpointer+1]))
						self.checkArr.append(False)
						self.typeText.set_text([ self.previousState,
												('netural', self.text[self.indexpointer+1:])])
						
						self.urwidloop.screen.clear()

					self.indexpointer +=1
				else:
					self.previousState.pop()
					self.indexpointer -=1
					self.typeText.set_text([ self.previousState,
												('netural', self.text[self.indexpointer:])])

					self.urwidloop.screen.clear()

		else:
			time = self.timerComponent.cancel_timer(task=self.Timertask)
			self.results = Results(checkarr=self.checkArr,
								   time=time
									   )
			self.parent.widget_list = [self.results.pile()]


	async def timer_done(self, *user_args):
		await self.Timertask
		time = self.timerComponent.cancel_timer(task=self.Timertask)
		self.results = Results(checkarr=self.checkArr,
								   time=time
									   )
		self.parent.widget_list = [self.results.pile()]

	def reset_test(self, *user_args):
		try:
			self.timerComponent.resetTimer(task=self.Timertask)
			self.cursorPlaceholder.set_edit_text('')
			
			self.indexpointer = 0
			self.previousState = []
			self.checkArr = []
			self.typeText.set_text(('netural', self.text))
			
			self.urwidloop.screen.clear()
		except AttributeError:
			pass	
			
	def new_test(self, *user_args):
		self.text = get_text()
		self.sentenceArr = list(self.text)

		self.reset_test()


		

	def exit(self, *user_args):
		raise urwid.ExitMainLoop()

		

