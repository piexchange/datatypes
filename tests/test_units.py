
import pickle

from datatypes.units import *


def test_dynamic_unit_is_only_instantiated_once():
    a = Megabytes / Seconds
    b = Megabytes / Seconds
    assert a is b


def test_dynamic_units_share_category():
    a = Megabytes / Seconds
    b = Gigabytes / Minutes
    assert a.category is b.category


def test_reordering():
    a = Bytes * Seconds
    b = Seconds * Bytes
    assert a is b


def test_simplification():
    assert Bytes * Seconds / Bytes is Seconds


def test_addition():
    a = Seconds(3)
    b = Minutes(2)
    assert a + b == Seconds(123)


def test_division():
    a = Bytes(10)
    b = Minutes(5)
    assert a / b == (Bytes/Minutes)(2)


def test_int_multiplication():
    a = Bytes(10)
    assert a * 5 == Bytes(50)


def test_int_multiplication_right():
    a = Bytes(10)
    assert 5 * a == Bytes(50)


def test_comparison():
    a = Minutes(1)
    b = Seconds(60)
    assert a == b


def test_instancecheck_same_class():
    a = Minutes(1)
    assert isinstance(a, Minutes)


def test_instancecheck_in_same_category():
    a = Minutes(1)
    assert not isinstance(a, Seconds)


def test_instancecheck_in_different_category():
    a = Minutes(1)
    assert not isinstance(a, Bytes)


def test_unit_conversion():
    a = Minutes(1)
    b = a.convert_to(Seconds)
    assert b.value == 60


def test_unit_str():
    unit = Megabytes
    val = unit(13)

    assert str(val) in {'13MB', '13 MB'}


def test_combined_unit_str():
    unit = Megabytes / Minutes
    val = unit(4)

    assert str(val) in {'4MB/min', '4 MB/min'}


def test_parse():
    text = '5 MB'
    val = Kilobytes.parse(text)

    assert val == Kilobytes(5000)


def test_pickling_base_unit():
    unit = Minutes(3)
    loaded_unit = pickle.loads(pickle.dumps(unit))

    assert unit == loaded_unit


def test_pickling_combined_unit():
    unit = (Megabytes/Minutes)(7)

    data = pickle.dumps(unit)
    loaded_unit = pickle.loads(data)

    assert unit == loaded_unit


def test_pickling_combined_unit_that_needs_to_be_created():
    unit = (Megabytes / Weeks)(7)

    data = pickle.dumps(unit)
    delattr(CombinedUnit, 'Megabytes/Weeks')
    loaded_unit = pickle.loads(data)

    assert unit == loaded_unit


def test_combined_unit_doesnt_pickle_too_much():
    unit = (Megabytes/Minutes)(7)

    data = pickle.dumps(unit)

    assert len(data) < 150
