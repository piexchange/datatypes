
from ..Type import Type

__all__ = ['Converter']


class Converter:
    def __new__(cls, type):
        if issubclass(type, Type):
            return type

        return super().__new__(cls)  # constructor is called implicitly

    def __init__(self, type):
        self.converter_func = _find_converter_func(type)

    def convert(self, value):
        return self.converter_func(value)


def _find_converter_func(type):
    try:
        return type._converter_func
    except AttributeError:
        return _DefaultConverter(type)


class _DefaultConverter:
    def __init__(self, type):
        self.type = type

    def __call__(self, value):
        if isinstance(value, self.type):
            return value

        raise TypeError("Cannot convert {} to a {}".format(value, self.type))
