def calculate_acc(checking_array):
	correct_chars = 0
	for char in checking_array:
		if char == True:
			correct_chars +=1

	return(float("{:.2f}".format((correct_chars/len(checking_array)*100))))

def word_per_min(checking_array, time):
	# imma use median word length
	wpm = (len(checking_array)/5)/(time/60)

	return(int(wpm))
