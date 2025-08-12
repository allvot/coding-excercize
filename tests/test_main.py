import pytest
from main import sort

@pytest.mark.parametrize("input, expected", [
    ((1, 2, 3, 4), "STANDARD"),
    ((100, 100, 100, 4), "SPECIAL"),
    ((1, 2, 3, 30), "SPECIAL"),
    ((1, 2, 3, 20), "SPECIAL"),
    ((100, 100, 100, 30), "REJECTED"),
    ((100, 100, 100, 20), "REJECTED"),
])

def test_sort(input, expected):
    assert sort(*input) == expected