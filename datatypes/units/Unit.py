
from .UnitValue import UnitValue


class Unit(type):
    _combined_units = {}

    def _get_combined_unit(self, other, op):
        unit_id = (self, op, other)
        try:
            return self._combined_units[unit_id]
        except KeyError:
            pass

        category_id = (self.category, op, other.category)
        try:
            category = self._combined_units[category_id]
        except KeyError:
            name = '{}{}{}'.format(self.category.__name__, op, other.category.__name__)
            category = type(self)(name, (), {})
            self._combined_units[category_id] = category

        if op == '/':
            name = '{}Per{}'.format(self.__name__, other.__name__[:-1].title())
        else:
            name = '{}{}{}'.format(self.__name__, op, other.__name__)
        bases = (category,)
        attrs = {'_abbr': '{}{}{}'.format(self._abbr, op, other._abbr),
                 '_value': self._value / other._value
                 }
        unit = type(self)(name, bases, attrs)
        self._combined_units[unit_id] = unit
        return unit

    @property
    def category(cls):
        return cls.__bases__[0]

    def __new__(mcs, *args, **kwargs):
        cls = super().__new__(mcs, *args, **kwargs)

        base = cls.__bases__[0]
        if base is object:
            cls._units = []
        else:
            base._units.append(cls)  # subclasses must be created from large to small

            if cls._value == 1:
                base._default = cls

        return cls

    def __call__(cls, value):
        value *= cls._value
        unit = cls.__bases__[0]
        return UnitValue(value, unit)

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
