
from datatypes import *


def test_subclasscheck():
    assert issubclass(bool, Boolean)


def test_subclasscheck_negative():
    assert not issubclass(int, Boolean)


def test_instancecheck():
    assert isinstance(True, Boolean)


def test_instancecheck_negative():
    assert not isinstance(5, Boolean)
