import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

from operations import add, subtract, multiply, divide
import pytest

def test_add():
    assert add(3, 2) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 0) == 0
    assert subtract(-1, -1) == 0

def test_multiply():
    assert multiply(4, 2) == 8
    assert multiply(0, 10) == 0
    assert multiply(-2, 3) == -6

def test_divide():
    assert divide(10, 2) == 5
    assert divide(-6, 3) == -2

    with pytest.raises(ValueError):
        divide(5, 0)