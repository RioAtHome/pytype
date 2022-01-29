import urwid

class Results:
	def __init__(self, checkarr, time):
		self.checkarr = checkarr
		self.time = time


	def calculate_acc(self):
		correctChars = 0
		for char in self.checkarr:
			if char == True:
				correctChars +=1

		return("{:.2f}".format((correctChars/len(self.checkarr)*100)))

	def word_per_min(self):

		# imma use median word length
		wpm = (len(self.checkarr)/5)/(self.time/60)

		return("{:.2f}".format(wpm))

	def pile(self):
		accWidget = urwid.Text(f'Accuracy:{self.calculate_acc()}%')
		wpmWidget = urwid.Text(f'Word Per Min:{str(self.word_per_min())}')
		exit = urwid.Button('Quit')

		urwid.connect_signal(exit, 'click', self.exit, user_args=[])

		pile = urwid.Pile([accWidget, wpmWidget, exit])

		return pile

	def exit(self, *user_args):
		raise urwid.ExitMainLoop()