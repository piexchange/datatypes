
import functools
import operator


class UnitMeta(type):
    _combined_units = {}

    def __new__(mcs, *args, is_category=False, **kwargs):
        cls = super().__new__(mcs, *args, **kwargs)

        if is_category:
            cls._units = []
        else:
            category = cls.category

            if category is not object:
                category._units.append(cls)  # subclasses must be created from large to small

                if cls._value == 1:
                    category._default = cls

        return cls

    @property
    def category(cls):
        return cls.__bases__[0]

    def _get_combined_unit(cls, other, op):
        unit_id = (cls, op, other)
        try:
            return cls._combined_units[unit_id]
        except KeyError:
            pass

        category_id = (cls.category, op, other.category)
        try:
            category = cls._combined_units[category_id]
        except KeyError:
            # create the category for this combined unit
            name = '{}{}{}'.format(cls.category.__name__, op, other.category.__name__)
            category = type(cls)(name, (Unit,), {}, is_category=True)
            cls._combined_units[category_id] = category

        if op == '/':
            name = '{}_per_{}'.format(cls.__name__, other.__name__[:-1])
        elif op == '*':
            name = '{}_times_{}'.format(cls.__name__, other.__name__)
        else:
            assert False, op
        bases = (category,)
        attrs = {'_abbr': '{}{}{}'.format(cls._abbr, op, other._abbr),
                 '_value': cls._value / other._value
                 }
        unit = type(cls)(name, bases, attrs)
        cls._combined_units[unit_id] = unit
        return unit

    def __mul__(self, other):
        return self._get_combined_unit(other, '*')

    def __truediv__(self, other):
        return self._get_combined_unit(other, '/')

    def format(cls, value):
        chunks = []

        for unit in cls._units:
            if value >= unit._value:
                num, value = divmod(value, unit._value)
                chunks.append('{}{}'.format(num, unit._abbr))

        if chunks:
            return ' '.join(chunks)

        return '0{}'.format(cls._default._abbr)


@functools.total_ordering
class Unit(metaclass=UnitMeta):
    def __init__(self, value):
        self.value = value

    @property
    def category(self):
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
        return type(self).format(self.value)
