
import pytest

import typing

import datatypes
from datatypes import python_type, typing_to_datatype


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
