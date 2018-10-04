
from typing import *

from datatypes import instancecheck


def test_basic_type():
    assert instancecheck(5, int)


def test_typing_type():
    assert instancecheck([], List)


def test_generic_iterable():
    assert instancecheck([1, 2], List[int])


def test_empty_iterable():
    assert instancecheck([], List[bool])


def test_generic_iterable_with_mixed_types():
    assert not instancecheck([1, 2.5], List[int])


def test_generic_mapping():
    assert instancecheck({1: 'foo'}, Dict[int, str])


def test_generic_mapping_detects_wrong_value_type():
    assert not instancecheck({1: 'foo'}, Dict[int, float])


def test_tuple():
    assert instancecheck(('bar', True), Tuple[str, bool])


def test_nested_generics():
    assert instancecheck(([1.5], 'bar'), Tuple[List[float], str])

