
from ..type import Type

__all__ = ['Converter']


class Converter:
    def __new__(cls, type_):
        if issubclass(type_, Type):
            return type_

        return super().__new__(cls)

    def __init__(self, type_):
        self.converter_func = _find_converter_func(type_)

    def convert(self, value):
        return self.converter_func(value)


def _find_converter_func(type_):
    try:
        return type_._converter_func
    except AttributeError:
        return _DefaultConverter(type_)


class _DefaultConverter:
    def __init__(self, type_):
        self.type = type_

    def __call__(self, value):
        if isinstance(value, self.type):
            return value

        raise TypeError("Cannot convert {} to a {}".format(value, self.type))
