
import pytest

from datatypes import *


# COLLECTIONS
def test_subscripting_generics():
    generic = List
    specific = generic[int]

    assert issubclass(specific, generic)


def test_subscripting_generics_with_nontypes():
    with pytest.raises(TypeError):
        List[5]


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


# OPTIONAL
def test_specializing_optional():
    assert issubclass(Optional[int], Optional)


def test_generic_optional_instancecheck():
    assert isinstance(5, Optional)


def test_specific_optional_instancecheck():
    assert isinstance(5, Optional[int])


def test_specific_optional_instancecheck_with_none():
    assert isinstance(None, Optional[int])


def test_parse_optional():
    assert Optional.parse(False) is False


def test_parse_specialized_optional():
    assert Optional[bool].parse(1) is True


def test_parse_specialized_optional_with_none():
    assert Optional[bool].parse(None) is None


def test_parse_specialized_optional_with_wrong_type():
    with pytest.raises(TypeError):
        Optional[list].parse(5)
