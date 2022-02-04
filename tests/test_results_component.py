import pytest
from ..widgets.results import Results

def test_calculate_acc_returns_correct_values():
	test_component_results = Results(checking_array=[True,
													 True,
													 True,
													 True,
													 True,
													 True,
													 True,
													 False,
													 True,
													 True,
													 True,
													 False,
													 True,
													 True,
													 True,
													 True,], time=5)

	assert test_component_results.calculate_acc() == "87.50"
	assert test_component_results.word_per_min() == "38.40"