def calculate_acc(checking_array):
    correct_chars = 0
    for char in checking_array:
        if char is True:
            correct_chars += 1

    return(float("{:.2f}".format((correct_chars / len(checking_array) * 100))))


def word_per_min(checking_array, time):
    if time == 0:
        time = 1

    try:
        wpm = (len(checking_array) / 5) / (time / 60)
    except ZeroDivisionError:
        ZeroDivisionError('wow, so fast')

    return(int(wpm))
