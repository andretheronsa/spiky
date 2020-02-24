import pytest

target = __import__("../../spiky")
spiky = target.spiky


def func(x):
    return x + 1


def test_answer():
    assert func(3) == 4
