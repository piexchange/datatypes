
import functools
import itertools
import operator
import re

"""
Class hierarchy and relationships:

*) unit categories (e.g. Memory, Duration) are instances of CategoryMeta
*) unit categories are class factories (metaclasses) that create unit classes
*) Unit is an instance of UnitMeta
*) unit classes (e.g. Bytes, Minutes) are subclasses of Unit
*) unit objects are instances of those classes
"""


class CategoryMeta(type):
    """
    Metaclass for unit categories.

    A unit category is another metaclass. However, using a unit category as a
    metaclass will create a UnitMeta instance - in other words, a Unit subclass.
    """

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)

        cls.units = []

    # using a category as metaclass will create a UnitMeta instance
    def __call__(cls, name, bases, attrs, unit_id=None):
        bases += (Unit,)
        unit = UnitMeta(name, bases, attrs, id_=unit_id)

        cls.units.append(unit)
        unit.category = cls

        if unit._value == 1:
            cls._default = unit

        return unit
    
    def __iter__(cls):
        return iter(cls.units)
    
    def lookup_abbr(cls, abbr):
        for unit in cls:
            if unit.abbr == abbr:
                return unit
        
        raise ValueError(abbr)

    def parse(cls, value):
        unit = cls._default
        return unit.parse(value)

    def format(cls, value):
        chunks = []

        for unit in cls.units:
            if value >= unit._value:
                num, value = divmod(value, unit._value)
                chunks.append('{} {}'.format(num, unit._abbr))

        if chunks:
            return ' '.join(chunks)

        return '0 {}'.format(cls._default._abbr)


class CombinedCategoryMeta(CategoryMeta):
    def format(cls, value):
        combinations = None

        for op, cat_dict in [(operator.mul, cls._id.mul), (operator.truediv, cls._id.div)]:
            for cat, count in cat_dict.items():
                for _ in range(count):
                    # if this is the first iteration of the loop, fill the combinations
                    # with the units in this category
                    if combinations is None:
                        combinations = {unit._value: (unit,) for unit in cat.units}
                        continue

                    # otherwise, create new combinations
                    combos = {}
                    for val, units in combinations.items():
                        for unit in cat.units:
                            us, v = (units + (unit,), op(val, unit._value))
                            if not 1 <= v <= value:
                                continue

                            # if multiple combinations have the same value, prefer
                            # the one that uses fewer different units
                            if v in us:
                                us = min(us, combos[v], key=lambda us: len(set(us)))

                            combos[v] = us
                    combinations = combos

        val, units = min(combinations.items(), key=lambda pair: value-pair[0])

        itr = iter(units)
        chunks = [next(itr)._abbr]
        for _ in range(sum(cls._id.mul.values()) - 1):
            unit = next(itr)
            chunks.append('*{}'.format(unit._abbr))
        for unit in itr:
            chunks.append('/{}'.format(unit._abbr))

        return '{} {}'.format(str(value / val), ''.join(chunks))


class UnitID:
    def __init__(self, mul, div):
        assert mul, mul

        self.mul = mul
        self.div = div

    @classmethod
    def for_base_unit(cls, unit):
        mul = {unit: 1}
        div = {}
        return cls(mul, div)

    @classmethod
    def merge(cls, id1, id2, op):
        mul1, div1 = id1
        mul2, div2 = id2
        if op == '/':
            mul2, div2 = div2, mul2

        mul = {k: mul1.get(k, 0) + mul2.get(k, 0) for k in mul1.keys() | mul2}
        div = {k: div1.get(k, 0) + div2.get(k, 0) for k in div1.keys() | div2}

        return cls(mul, div)

    def __eq__(self, other):
        if not isinstance(other, __class__):
            return NotImplemented

        return self.mul == other.mul and self.div == other.div

    def __hash__(self):
        return hash(tuple(frozenset(dic.items()) for dic in self))

    def to_category_id(self):
        dicts = [{k.category: v for k, v in dic.items()} for dic in self]
        cat_id = type(self)(*dicts)
        return cat_id.normalized()

    def __iter__(self):
        yield self.mul
        yield self.div

    def normalized(self):
        mul, div = self

        shared_keys = mul.keys() & div
        shared_units = {key: min(mul[key], div[key]) for key in shared_keys}

        norm_id = []
        for dic in (mul, div):
            dic = {unit: count - shared_units.get(unit, 0) for unit, count in dic.items()}
            dic = {unit: count for unit, count in dic.items() if count > 0}

            norm_id.append(dic)

        return type(self)(*norm_id)

    def _reduce(self, map_func, merge_func):
        itr = iter(self.mul.items())

        unit, count = next(itr)
        accu = unit = map_func(unit)
        for _ in range(count-1):
            accu = merge_func('*', accu, unit)

        for op, itr in [('*', itr), ('/', self.div.items())]:
            for unit, count in itr:
                unit = map_func(unit)

                for _ in range(count):
                    accu = merge_func(op, accu, unit)

        return accu

    def _attr_from_id(self, attr):
        map_func = operator.attrgetter(attr)

        def merge_func(op, unit1, unit2):
            return '{}{}{}'.format(unit1, op, unit2)

        return self._reduce(map_func, merge_func)

    def generate_name(self):
        return self._attr_from_id('__name__')

    def generate_abbr(self):
        return self._attr_from_id('_abbr')

    def generate_value(self):
        map_func = operator.attrgetter('_value')

        def merge_func(op, unit1, unit2):
            op = {
                '*': operator.mul,
                '/': operator.truediv
            }[op]
            return op(unit1, unit2)

        return self._reduce(map_func, merge_func)

    def __repr__(self):
        def prettify_dict(dic):
            return {unit.__name__: count for unit, count in dic.items()}

        dicts = map(prettify_dict, self)

        return '{}({}, {})'.format(type(self).__name__, *dicts)


class UnitMeta(type):
    """
    Metaclass for all Units. This is where multiplication and division of Units is implemented.
    """

    _units_by_id = {}

    def __new__(mcs, *args, id_=None, **kwargs):
        return super().__new__(mcs, *args, **kwargs)

    def __init__(cls, *args, id_=None, **kwargs):
        super().__init__(*args, **kwargs)

        if id_ is None:
            id_ = UnitID.for_base_unit(cls)
        cls._id = id_

        cls._units_by_id[id_] = cls

        # for pickle support, all Unit subclasses can be accessed as attributes of the CombinedUnit namespace object
        setattr(CombinedUnit, cls.__name__, cls)

    def __mul__(cls, other):
        return CombinedUnitFactory.merge(cls, other, '*')

    def __truediv__(cls, other):
        return CombinedUnitFactory.merge(cls, other, '/')


class CombinedUnitFactory(type):
    # this is only a metaclass because pickle doesn't allow attribute lookup on non-classes.
    """
    A factory that creates units of combined types (like bytes per second).

    The single argument accepted by the factory is the combined unit's ID. This ID is
    a tuple of two dicts:

        ID = (multiply_dict, divide_dict)

    And the two dicts hold unit:quantity pairs. For example, bytes per second would
    be represented as ({Bytes: 1}, {Seconds: 1}). Similarly, bytes per second squared
    would be represented as ({Bytes: 1}, {Seconds: 2}).

    The ID is automatically normalized. (In other words, ({A: 2}, {A: 1}) is equivalent to ({A: 1}, {}).)
    """

    _combined_categories = {}

    # calling this class returns a Unit instance
    def __new__(mcs, unit_id):
        unit_id = unit_id.normalized()
        try:
            return UnitMeta._units_by_id[unit_id]
        except KeyError:
            pass

        # first, get (or create) the appropriate category for this new unit
        category_id = unit_id.to_category_id()
        try:
            category = mcs._combined_categories[category_id]
        except KeyError:
            # create the category for this combined unit
            name = category_id.generate_name()
            attrs = {
                '_id': category_id
            }
            category = CombinedCategoryMeta(name, (), attrs)
            mcs._combined_categories[category_id] = category

        # now that we have the appropriate category, create the new unit
        name = unit_id.generate_name()
        bases = ()
        attrs = {
            '_abbr': unit_id.generate_abbr(),
            '_value': unit_id.generate_value(),
        }
        unit = category(name, bases, attrs, unit_id=unit_id)
        unit.__qualname__ = '{}.{}'.format(CombinedUnit.__qualname__, name)

        return unit

    @classmethod
    def merge(mcs, unit1, unit2, op):
        unit_id = UnitID.merge(unit1._id, unit2._id, op)
        return mcs(unit_id)

    def __getattr__(cls, attr):
        # This method exists for pickle support, which looks up classes based on their qualname.
        # Given the name of a combined unit as input, an appropriate class must be created and returned.
        if '*' not in attr and '/' not in attr:
            raise AttributeError

        def get_unit(name):
            try:
                return vars(cls)[name]
            except KeyError:
                raise AttributeError

        # split the name into a series of unit names and operators
        unit_id = re.split(r'([*/])', attr)
        itr = iter(unit_id)

        unit = get_unit(next(itr))
        for op in itr:
            op = {
                '*': operator.mul,
                '/': operator.truediv
            }[op]

            next_unit = get_unit(next(itr))

            unit = op(unit, next_unit)

        return unit


# create a namespace class that allows access to all combined units as attributes.
# pickle doesn't support attribute lookup on non-classes, so CombinedUnit has to be a class.
CombinedUnit = type.__new__(CombinedUnitFactory, 'CombinedUnit', (), {})  # skip calling CombinedUnitFactory.__new__


@functools.total_ordering
class Unit(metaclass=UnitMeta):
    """
    Base class for all Units.
    """

    def __init__(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('unit value must be an int or float, not {}'.format(type(value)))

        self.value = value
    
    @classmethod
    def parse(cls, value):
        total = cls(0)
        
        category = cls.category
        units_by_abbr = {unit._abbr: unit for unit in category}
        
        val = value
        while val:
            match = re.match(r'(\d+(?:\.\d+)?) ?([^\d\s]+) ?', val)
            if not match:
                raise ValueError('Cannot parse string "{}"'.format(value))
            val = val[match.end():]
            
            num = match.group(1)
            abbr = match.group(2)
            if '.' in num:
                num = float(num)
            else:
                num = int(num)

            try:
                unit = units_by_abbr[abbr]
            except KeyError:
                raise ValueError('Cannot parse string "{}": unknown unit "{}"'.format(value, abbr))

            total += unit(num)

        return total
    
    @classmethod
    def lookup_abbr(cls, abbr):
        for unit in cls.__subclasses__():
            if unit.abbr == abbr:
                return unit
        
        raise ValueError(abbr)

    @property
    def category(self):
        """
        The unit's category; i.e. what the unit measures.

        Examples for unit categories are time, length, speed, volume, etc.

        :return: A class representing the unit's category
        :rtype: type
        """
        return type(self).category

    def convert_to(self, unit):
        if self.category != unit.category:
            raise TypeError("Cannot convert {} to {}".format(type(self), unit))

        value = self.value * (type(self)._value / unit._value)
        return unit(value)

    def __add__(self, other):
        return self._addsub(other, operator.add, 'add')

    def __sub__(self, other):
        return self._addsub(other, operator.sub, 'subtract')

    def __radd__(self, other):
        return self.__add__(other)

    def _addsub(self, other, op, opname):
        if not isinstance(other, __class__):
            return NotImplemented

        if self.category != other.category:
            raise TypeError('Cannot {} {} and {}'.format(opname, type(self), type(other)))

        other_val = other.value * other._value / self._value
        value = op(self.value, other_val)
        return type(self)(value)

    def __mul__(self, other):
        return self._muldiv(other, operator.mul, 'multiply')

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return self._muldiv(other, operator.truediv, 'divide')

    def _muldiv(self, other, op, opname):
        if isinstance(other, (int, float)):
            value = op(self.value, other)
            return type(self)(value)

        if not isinstance(other, __class__):
            return NotImplemented

        cls = op(type(self), type(other))
        value = op(self.value, other.value)
        return cls(value)

    def __eq__(self, other):
        if not isinstance(other, __class__):
            return NotImplemented

        if self.category != other.category:
            return False

        return self.value * type(self)._value == other.value * type(other)._value

    def __lt__(self, other):
        if not isinstance(other, __class__):
            return NotImplemented

        if self.category != other.category:
            raise TypeError("Can't compare {} to {}".format(type(self), type(other)))

        return self.value * type(self)._value < other.value * type(other)._value

    def multi_unit_str(self):
        return self.category.format(self.value * type(self)._value)

    def __int__(self):
        return int(self.value * type(self)._value)

    def __float__(self):
        return float(self.value * type(self)._value)

    def __repr__(self):
        return '{} {}'.format(self.value, type(self)._abbr)
