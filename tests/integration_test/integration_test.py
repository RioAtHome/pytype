import pytest
from ...main import Main


@pytest.mark.filterwarnings('ignore::RuntimeWarning')
def test_reset_test_clears_():
    test_main_component = Main(text='The quick', timer=10)

    test_main_component.type_checking(_=None, string_typed="T")
    test_main_component.type_checking(_=None, string_typed="Th")
    test_main_component.type_checking(_=None, string_typed="Thy")
    test_main_component.type_checking(_=None, string_typed="Thy ")
    test_main_component.type_checking(_=None, string_typed="Thy Q")

    test_main_component._reset_test()

    expected_tuple = ('The quick\n', [('netural', 10)])

    assert test_main_component.timer_componenet.time_count == 10
    assert test_main_component.typing_component.get_text() == expected_tuple


@pytest.mark.filterwarnings('ignore::RuntimeWarning')
def test_new_test_generates_new_text():
    test_main_component = Main(text="The quick", timer=10)

    test_main_component._new_test()

    new_text = test_main_component.typing_component.get_text()

    assert 'The quick\n' not in new_text


@pytest.mark.filterwarnings('ignore::RuntimeWarning')
def test_results_widget():
    test_main_component = Main(text="Test1", timer=2)

    test_main_component.type_checking(_=None, string_typed="T")
    test_main_component.type_checking(_=None, string_typed="Te")
    test_main_component.type_checking(_=None, string_typed="Tes")
    test_main_component.type_checking(_=None, string_typed="TesT")
    test_main_component.type_checking(_=None, string_typed="TesT1")

    pile = test_main_component.main_pile.widget_list

    assert test_main_component.container_results in pile
