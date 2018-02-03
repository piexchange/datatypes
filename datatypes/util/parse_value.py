
from ..Type import Type
from ..types.Boolean import Boolean


def parse_value(value, type):
    if isinstance(type, Type):
        return type.convert(value)

    if issubclass(type, bool):
        return Boolean().convert(value)

    return type(value)
    # raise TypeError('Unable to convert "{}" to {}'.format(value, type))
