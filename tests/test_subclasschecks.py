
from typing import *

from datatypes import is_subtype


def test_basic_type():
    assert is_subtype(bool, int)


def test_typing_type():
    assert is_subtype(list, List)


def test_generic_iterable():
    assert is_subtype(List[int], list)


def test_generic_mapping():
    assert is_subtype(Dict[int, str], dict)


def test_mismatched_generic_mapping():
    assert not is_subtype(Dict[int, str], Dict[int, float])


def test_tuple():
    assert is_subtype(Tuple[str, bool], tuple)


def test_nested_generics():
    assert is_subtype(Tuple[List[float]], Tuple[list])
