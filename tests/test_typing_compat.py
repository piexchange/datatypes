
import pytest

import typing

import datatypes
from datatypes import is_generic, is_base_generic, is_qualified_generic, class_to_datatype


@pytest.mark.parametrize(['cls', 'dtype'], [
    (bytearray, bytearray),
    (int, datatypes.Integer),
    (typing.Text, datatypes.Text),
    (typing.List, datatypes.List),
    (typing.Dict, datatypes.Dict),
    (typing.List[bytearray], datatypes.List[bytearray]),
    (typing.List[typing.Dict], datatypes.List[datatypes.Dict]),
    (typing.List[typing.Dict[bytearray, memoryview]], datatypes.List[datatypes.Dict[bytearray, memoryview]]),
])
def test_class_to_datatype(cls, dtype):
    assert class_to_datatype(cls) == dtype


@pytest.mark.parametrize(['type_', 'expected'], [
    (int, False),
    (list, False),
    (typing.Any, False),
    (typing.List, True),
    (typing.Union, True),
    (typing.Callable, True),
    (typing.Optional, True),
    (typing.List[int], True),
    (typing.Union[int, str], True),
    (typing.Callable[[], int], True),
    (typing.Optional[int], True),
])
def test_is_generic(type_, expected):
    assert is_generic(type_) == expected


@pytest.mark.parametrize(['type_', 'expected'], [
    (int, False),
    (list, False),
    (typing.Any, False),
    (typing.List, True),
    (typing.Union, True),
    (typing.Callable, True),
    (typing.Optional, True),
    (typing.List[int], False),
    (typing.Union[int, str], False),
    (typing.Callable[[], int], False),
    (typing.Optional[int], False),
])
def test_is_base_generic(type_, expected):
    assert is_base_generic(type_) == expected


@pytest.mark.parametrize(['type_', 'expected'], [
    (int, False),
    (list, False),
    (typing.Any, False),
    (typing.List, False),
    (typing.Union, False),
    (typing.Callable, False),
    (typing.Optional, False),
    (typing.List[int], True),
    (typing.Union[int, str], True),
    (typing.Callable[[], int], True),
    (typing.Optional[int], True),
])
def test_is_qualified_generic(type_, expected):
    assert is_qualified_generic(type_) == expected
