
import collections
import typing

from .collection import CollectionMeta
from .type import Type
from ..parse import parse

__all__ = ['Dict']


class Dict(Type, metaclass=CollectionMeta, subtype_names=['key_type', 'value_type']):
    python_type = dict
    typing_type = typing.Dict

    @classmethod
    def parse(cls, value):
        python_type = cls.python_type

        if isinstance(value, python_type):
            value = value.items()
        elif isinstance(value, (str, bytes)):
            value = value.split()
            value = (pair.split('=', 1) for pair in value)
        elif isinstance(value, collections.iterable):
            pass
        else:
            raise TypeError('Expected a dict of {} -> {}, got {}'.format(self.key_type, self.value_type, type(value)))

        key_converter = lambda key: parse(key, cls.key_type)
        value_converter = lambda value: parse(value, cls.value_type)
        value = python_type((key_converter(k), value_converter(v)) for k, v in value)
        return value