import pytest
from ..widgets.typing import Typing

def test_check_input_at_null():
	with pytest.raises(TypeError):
		Typing()

def test_check_input_at_empty_string():
	assert Typing("Hello World!").check_input("") == True

def test_check_input_adding_correct_input():
	test_component_typing = Typing("Hello World!")
	test_component_typing.check_input("H")

	assert test_component_typing.checking_array[0] == True

def test_check_input_adding_wrong_input():
	test_component_typing = Typing("Hello World!")
	test_component_typing.check_input("h")
	test_component_typing.check_input("")
	test_component_typing.check_input("H")

	assert test_component_typing.checking_array[0] == False

def test_check_input_moves_pointer():	
	test_component_typing = Typing("Hello World!")
	test_component_typing.check_input("h")

	assert test_component_typing.cursor_pointer == 1

def test_check_input_generates_correct_previous_state():
	test_component_typing = Typing("Hello World!")
	test_component_typing.check_input("h")
	test_component_typing.check_input("hE")
	test_component_typing.check_input("hEl")
	test_component_typing.check_input("hEll")

	expected_previous_state = [('wronginput', 'H'),
							   ('wronginput', 'e'),
							   ('rightinput', 'l'),
							   ('rightinput', 'l'),
							   ]

	assert test_component_typing.previous_state == expected_previous_state

def test_check_input_input_then_backspace():
	test_component_typing = Typing("Hello World!")
	test_component_typing.check_input("h")
	test_component_typing.check_input("")
	test_component_typing.check_input("H")

	assert test_component_typing.typing_start == False

def test_check_input_return_false_at_end_of_string():
	test_component_typing = Typing("Hello!")
	test_component_typing.check_input("h")
	test_component_typing.check_input("he")
	test_component_typing.check_input("heL")
	test_component_typing.check_input("heLl")
	test_component_typing.check_input("heLlo")

	assert test_component_typing.check_input("heLlo!") == False


def test_get_results_returns_expected_array():
	test_component_typing = Typing("Hell")
	test_component_typing.check_input("h")
	test_component_typing.check_input("he")
	test_component_typing.check_input("heL")
	test_component_typing.check_input("heLl")

	expected_checking_array = [False, True, False, True]

	assert test_component_typing.get_results() == expected_checking_array	


