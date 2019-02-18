
from typing import *

from datatypes import is_instance


def test_basic_type():
    assert is_instance(5, int)


def test_typing_type():
    assert is_instance([], List)


def test_generic_iterable():
    assert is_instance([1, 2], List[int])


def test_empty_iterable():
    assert is_instance([], List[bool])


def test_generic_iterable_with_mixed_types():
    assert not is_instance([1, 2.5], List[int])


def test_generic_mapping():
    assert is_instance({1: 'foo'}, Dict[int, str])


def test_generic_mapping_detects_wrong_value_type():
    assert not is_instance({1: 'foo'}, Dict[int, float])


def test_tuple():
    assert is_instance(('bar', True), Tuple[str, bool])


def test_nested_generics():
    assert is_instance(([1.5], 'bar'), Tuple[List[float], str])


