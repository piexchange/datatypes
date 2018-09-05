
import operator
import functools


@functools.total_ordering
class UnitValue:
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

    def __add__(self, other):
        return self._addsub(other, operator.add, 'add')

    def __sub__(self, other):
        return self._addsub(other, operator.sub, 'subtract')

    def _addsub(self, other, op, opname):
        if not isinstance(other, __class__):
            raise TypeError
        if self.unit != other.unit:
            raise TypeError('Cannot {} {} and {}'.format(opname, self.unit, other.unit))

        value = op(self.value, other.value)
        return __class__(value, self.unit)

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return __class__(other, self.unit) - self

    def __mul__(self, other):
        if not isinstance(other, __class__):
            return __class__(self.value * other, self.unit)

        value = self.value * other.value
        unit = self.unit * other.unit
        return __class__(value, unit)

    def __truediv__(self, other):
        if not isinstance(other, __class__):
            return __class__(self.value / other, self.unit)

        value = self.value / other.value
        unit = self.unit / other.unit
        return __class__(value, unit)

    def __eq__(self, other):
        if not isinstance(other, __class__):
            return NotImplemented

        if self.unit != other.unit:
            return False

        return self.value == other.value

    def __lt__(self, other):
        if not isinstance(other, __class__):
            return NotImplemented

        if self.unit != other.unit:
            return NotImplemented

        return self.value < other.value

    def __repr__(self):
        return self.unit.format(self.value)
