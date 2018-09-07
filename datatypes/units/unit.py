
import functools
import operator
import re


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
    def __call__(cls, name, bases, attrs):
        bases += (Unit,)
        unit = UnitMeta(name, bases, attrs)

        cls.units.append(unit)
        unit.category = cls

        if unit._value == 1:
            cls._default = unit

        return unit

    def format(cls, value):
        chunks = []

        for unit in cls.units:
            if value >= unit._value:
                num, value = divmod(value, unit._value)
                chunks.append('{}{}'.format(num, unit._abbr))

        if chunks:
            return ' '.join(chunks)

        return '0{}'.format(cls._default._abbr)


class UnitMeta(type):
    """
    Metaclass for all Units. This is where multiplication and division of Units is implemented.
    """
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cls._id = cls

        # for pickle support, all Unit subclasses can be accessed as attributes of the CombinedUnit namespace object
        setattr(CombinedUnit, cls.__name__, cls)

    def __mul__(cls, other):
        return CombinedUnitFactory.merge(cls, other, '*')

    def __truediv__(cls, other):
        return CombinedUnitFactory.merge(cls, other, '/')


class CombinedUnitFactory(type):
    _combined_units = {}
    _combined_categories = {}

    # calling this class returns a Unit instance
    def __new__(cls, unit_id):
        unit_id = cls._normalize_id(unit_id)
        try:
            return cls._combined_units[unit_id]
        except KeyError:
            pass

        # first, get (or create) the appropriate category for this new unit
        category_id = cls._get_category_id(unit_id)
        try:
            category = cls._combined_categories[category_id]
        except KeyError:
            # create the category for this combined unit
            name = cls._name_from_id(category_id)
            category = CategoryMeta(name, (), {})
            cls._combined_categories[category_id] = category

        # now that we have the appropriate category, create the new unit
        name = cls._name_from_id(unit_id)
        bases = ()
        attrs = {
            '_abbr': cls._abbr_from_id(unit_id),
            '_value': cls._value_from_id(unit_id)
        }
        unit = category(name, bases, attrs)
        unit.__qualname__ = '{}.{}'.format(CombinedUnit.__qualname__, name)

        cls._combined_units[unit_id] = unit
        return unit

    @classmethod
    def merge(cls, unit1, unit2, op):
        unit_id = (op, unit1, unit2)
        return cls(unit_id)

    @staticmethod
    def _normalize_id(unit_id):
        return unit_id  # TODO

    @classmethod
    def _get_category_id(cls, unit_id):
        def categorize(id_):
            if isinstance(id_, tuple):
                return (id_[0], *map(categorize, id_[1:]))
            return id_.category

        category_id = categorize(unit_id)
        return cls._normalize_id(category_id)

    @classmethod
    def _reduce_id(cls, unit_id, map_func, merge_func):
        if isinstance(unit_id, tuple):
            op, *units = unit_id
            units = [cls._reduce_id(unit, map_func, merge_func) for unit in units]
            return functools.reduce(lambda x, y: merge_func(op, x, y), units)
        else:
            return map_func(unit_id)

    @classmethod
    def _attr_from_id(cls, unit_id, attr):
        map_func = operator.attrgetter(attr)

        def merge_func(op, unit1, unit2):
            return '{}{}{}'.format(unit1, op, unit2)

        return cls._reduce_id(unit_id, map_func, merge_func)

    @classmethod
    def _name_from_id(cls, unit_id):
        return cls._attr_from_id(unit_id, '__name__')

    @classmethod
    def _abbr_from_id(cls, unit_id):
        return cls._attr_from_id(unit_id, '_abbr')

    @classmethod
    def _value_from_id(cls, unit_id):
        map_func = operator.attrgetter('_value')

        def merge_func(op, unit1, unit2):
            op = {
                '*': operator.mul,
                '/': operator.truediv
            }[op]
            return op(unit1, unit2)

        return cls._reduce_id(unit_id, map_func, merge_func)

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
        self.value = value

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

    def _addsub(self, other, op, opname):
        if not isinstance(other, __class__):
            return NotImplemented

        if self.category != other.category:
            raise TypeError('Cannot {} {} and {}'.format(opname, type(self), type(other)))

        value = op(self.value, other.value)
        return type(self)(value)

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        return self._muldiv(other, operator.mul, 'multiply')

    def __truediv__(self, other):
        return self._muldiv(other, operator.truediv, 'divide')

    def _muldiv(self, other, op, opname):
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

    def __repr__(self):
        return self.category.format(self.value)
