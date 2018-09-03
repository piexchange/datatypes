
from ..type import Type
from ..types.Boolean import Boolean


def parse(value, type_):
    if Type in type_.mro():
        return type_.parse(value)

    if issubclass(type_, bool):
        return Boolean.parse(value)

    return type_(value)
    # raise TypeError('Unable to convert "{}" to {}'.format(value, type))
