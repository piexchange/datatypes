
from datatypes import units
from datatypes.units import *


def test_dynamic_unit_is_only_instantiated_once():
    a = megabytes / seconds
    b = megabytes / seconds
    assert a is b


def test_dynamic_units_share_category():
    a = megabytes / seconds
    b = gigabytes / minutes
    assert a.category is b.category


def test_addition():
    a = minutes(3)
    b = minutes(5)
    assert a + b == minutes(8)


def test_division():
    a = units.bytes(10)
    b = minutes(5)
    assert a / b == (units.bytes/minutes)(2)
