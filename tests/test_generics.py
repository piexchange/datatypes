
import pytest
from conftest import depends_on

from datatypes import *


def test_subscripting_generics():
    generic = List
    specific = generic[int]

    assert issubclass(specific, generic)


def test_subscripting_generics_with_nontypes():
    with pytest.raises(TypeError):
        List[5]


@depends_on(test_subscripting_generics)
# @pytest.mark.depends_on(test_subscripting_generics)
def test_subscripting_specifics():
    specific = List[int]

    with pytest.raises(TypeError):
        specific[bool]


def test_generic_instancecheck():
    assert isinstance([1, 2], List)


def test_specific_instancecheck():
    assert isinstance([1, 2], List[int])


def test_specific_instancecheck_negative():
    assert not isinstance([1, 2], List[bool])


def test_generic_conversion():
    assert Set.parse([1, 2]) == {1, 2}


def test_specific_conversion():
    assert Set[int].parse([1.5, 2.3]) == {1, 2}
