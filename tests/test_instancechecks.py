
import pytest

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


def test_any():
    assert is_instance(5, Any)


if 'Type' in globals():  # for some reason Type doesn't exist in 3.5.0 even though it's documented
    @pytest.mark.parametrize('value, type_, expected', [
        (int, Type, True),
        (type, Type, True),
        (int, Type[int], True),
        (int, Type[float], False),
        (bool, Type[int], True),
    ])
    def test_type(value, type_, expected):
        assert is_instance(value, type_) == expected


@pytest.mark.parametrize('value, type_, expected', [
    ('foo', Union[int, str, bytearray], True),
    ('foo', Union[int, bytearray], False),
])
def test_union(value, type_, expected):
    assert is_instance(value, type_) == expected


def int_str__float(i: int, s: str) -> float:
    pass

unannotated_func = lambda i: None
unannotated_func.__name__ = 'unannotated_func'

def unannotated_retval(i: int):
    pass

def unannotated_param(i) -> float:
    pass

@pytest.mark.parametrize('value, type_, expected', [
    (unannotated_func, Callable, True),
    (unannotated_retval, Callable, True),
    (unannotated_param, Callable, True),
    (int_str__float, Callable, True),
    (int_str__float, Callable[[int, str], float], True),
    (int_str__float, Callable[[int], float], False),
    (int_str__float, Callable[[int, str, bool], float], False),
    (int_str__float, Callable[..., float], True),
])
def test_callable(value, type_, expected):
    assert is_instance(value, type_) == expected


@pytest.mark.parametrize('value, type_', [
    (unannotated_func, Callable[[int], None]),
    (unannotated_retval, Callable[[int], None]),
    (unannotated_param, Callable[[int], float]),
])
def test_unannotated_callable(value, type_):
    with pytest.raises(ValueError):
        is_instance(value, type_)


T = TypeVar('T')

def t__t(x: T) -> T:
    pass

def t_t__t(x: T, y: T) -> T:
    pass

# @pytest.mark.parametrize('value, type_, expected', [
#     (t__t, Callable, True),
#     (t__t, Callable[[int], int], True),
#     (t__t, Callable[[int], bool], True),
#     (t__t, Callable[[bool], int], True),
#     (t__t, Callable[[int], float], False),
#     (t_t__t, Callable[[int, int], int], True),
#     (t_t__t, Callable[[int, bool], bool], True),
#     (t_t__t, Callable[[bool, bool], int], True),
#     (t_t__t, Callable[[int, bool], float], False),
# ])
# def test_callable_with_typevars(value, type_, expected):
#     assert is_instance(value, type_) == expected
