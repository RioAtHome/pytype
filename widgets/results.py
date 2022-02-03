import urwid

class Results(urwid.Pile):
	def __init__(self, checking_array, time):
		self.checking_array = checking_array
		self.time = time
		self.acc_widget = urwid.Text(f'Accuracy:{self.calculate_acc()}%')
		self.wpm_widget = urwid.Text(f'Word Per Min:{str(self.word_per_min())}')
		self.exit = urwid.Button('Quit')

		super().__init__([self.acc_widget, self.wpm_widget])

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
