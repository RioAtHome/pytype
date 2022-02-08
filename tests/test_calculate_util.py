from ..util.calculate_util import calculate_acc, word_per_min


def test_calculate_util_returns_correct_values():

    test_component_results = [
        True, True, True, True,
        True, True, True, False, True, True, True,
        False, True, True, True, True]

    assert calculate_acc(test_component_results) == 87.50
    assert word_per_min(test_component_results, time=5) == 38
