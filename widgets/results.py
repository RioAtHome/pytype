import urwid

class Results:
	def __init__(self, checking_array, time):
		self.checking_array = checking_array
		self.time = time


	def calculate_acc(self):
		correct_chars = 0
		for char in self.checking_array:
			if char == True:
				correct_chars +=1

		return("{:.2f}".format((correct_chars/len(self.checking_array)*100)))

	def word_per_min(self):

		# imma use median word length
		wpm = (len(self.checking_array)/5)/(self.time/60)

		return("{:.2f}".format(wpm))

	def pile(self):
		acc_widget = urwid.Text(f'Accuracy:{self.calculate_acc()}%')
		wpm_widget = urwid.Text(f'Word Per Min:{str(self.word_per_min())}')
		exit = urwid.Button('Quit')

		urwid.connect_signal(exit, 'click', self.exit, user_args=[])

		pile = urwid.Pile([acc_widget, wpm_widget, exit])

		return pile

	def exit(self, *user_args):
		raise urwid.ExitMainLoop()