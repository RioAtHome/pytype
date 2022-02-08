import urwid
import logging

logging.basicConfig(filename='example.log')


class Typing(urwid.Edit):
    def __init__(self, sentence_string):
        self.sentence_string = sentence_string + '\n'
        self.sentence_array = list(sentence_string)

        self.checking_array = []
        self.previous_state = []
        self.cursor_pointer = 0
        self.typing_start = True

        super().__init__(caption=('netural', self.sentence_string), edit_text='')

    def check_input(self, string_typed):
        if self.cursor_pointer != len(self.sentence_array) - 1:
            # Beginning of the sentence
            # Yes
            if self.cursor_pointer == 0:
                self.input_char = string_typed
                # is input_char correct?

                if self.input_char == self.sentence_array[self.cursor_pointer]:
                    self.previous_state.append(('rightinput',
                                                self.sentence_string[self.cursor_pointer:self.cursor_pointer+1]
                                                ))

                    self.checking_array.append(True)

                    super().set_caption([self.previous_state,
                                        ('netural', self.sentence_string[self.cursor_pointer+1:])])

                elif self.input_char != self.sentence_array[self.cursor_pointer]:
                    self.previous_state.append(('wronginput',
                                                self.sentence_string[self.cursor_pointer:self.cursor_pointer+1]))
                    self.checking_array.append(False)
                    super().set_caption([self.previous_state,
                                        ('netural', self.sentence_string[self.cursor_pointer+1:])])
                self.cursor_pointer += 1

                if(self.typing_start):
                    self.typing_start = False
                    return True

                return

            # No
            else:
                if len(string_typed) >= self.cursor_pointer:

                    self.input_char = string_typed[self.cursor_pointer]

                    if self.input_char == self.sentence_array[self.cursor_pointer]:
                        self.checking_array.append(True)
                        self.previous_state.append(('rightinput',
                                                    self.sentence_string[self.cursor_pointer:self.cursor_pointer+1]))

                        super().set_caption([self.previous_state,
                                            ('netural', self.sentence_string[self.cursor_pointer+1:])])

                    else:
                        self.previous_state.append(('wronginput',
                                                    self.sentence_string[self.cursor_pointer:self.cursor_pointer+1]))
                        self.checking_array.append(False)
                        super().set_caption([self.previous_state,
                                            ('netural', self.sentence_string[self.cursor_pointer+1:])])

                    self.cursor_pointer += 1
                else:
                    self.previous_state.pop()
                    self.cursor_pointer -= 1
                    super().set_caption([self.previous_state,
                                        ('netural', self.sentence_string[self.cursor_pointer:])])

            return
        # Reached end of sentence.
        else:
            self.input_char = string_typed[self.cursor_pointer]

            if self.input_char == self.sentence_array[self.cursor_pointer]:
                self.checking_array.append(True)

            else:
                self.checking_array.append(False)

            return(self.typing_start)

    def get_results(self):
        if self.checking_array == []:
            return

        return(self.checking_array)

    def reset_test(self):
        self.checking_array = []
        self.previous_state = []
        self.cursor_pointer = 0
        self.typing_start = True

        super().set_caption(('netural', self.sentence_string))
        super().set_edit_text('')

    def new_test(self, sentence_string):
        self.sentence_string = sentence_string + '\n'
        self.sentence_array = list(sentence_string)

        self.checking_array = []
        self.previous_state = []
        self.cursor_pointer = 0
        self.typing_start = True

        super().set_caption(self.sentence_string)
        super().set_edit_text('')
