
import pytest

import typing

import datatypes
from datatypes import typing_to_datatype, is_generic, is_base_generic, is_qualified_generic


@pytest.mark.parametrize(['typing_annotation', 'datatype'], [
    [int, int],
    [str, str],
    [typing.List, datatypes.List],
    [typing.List[int], datatypes.List[int]],
    [typing.List[typing.Dict], datatypes.List[datatypes.Dict]],
    [typing.List[typing.Dict[int, str]], datatypes.List[datatypes.Dict[int, str]]],
])
def test_typing_to_datatype(typing_annotation, datatype):
    assert typing_to_datatype(typing_annotation) == datatype


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
def test_is_specialized_generic(type_, expected):
    assert is_qualified_generic(type_) == expected
