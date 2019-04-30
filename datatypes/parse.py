
from .types import Type


__all__ = ['parse']


def parse(value, type_):
    from .type_compat import class_to_datatype  # this import has to be here to avoid cyclic imports at import time

    type_ = class_to_datatype(type_)

    if isinstance(type_, type) and issubclass(type_, Type):
        return type_.parse(value)

    return type_(value)
    # raise TypeError('Unable to convert "{}" to {}'.format(value, type))
