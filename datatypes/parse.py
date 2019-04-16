
from .types import Type, Boolean
from .type_compat import typing_to_datatype


__all__ = ['parse']


def parse(value, type_):
    type_ = typing_to_datatype(type_)

    if issubclass(type_, Type):
        return type_.parse(value)

    if issubclass(type_, bool):
        return Boolean.parse(value)

    return type_(value)
    # raise TypeError('Unable to convert "{}" to {}'.format(value, type))
