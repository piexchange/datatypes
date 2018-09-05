
from ..types import Type, Boolean


def parse(value, type_):
    if issubclass(type_, Type):
        return type_.parse(value)

    if issubclass(type_, bool):
        return Boolean.parse(value)

    return type_(value)
    # raise TypeError('Unable to convert "{}" to {}'.format(value, type))
