
import collections

from .collection import CollectionMeta
from ..util import parse

__all__ = ['Dict']


class Dict(metaclass=CollectionMeta, subtype_names=['key_type', 'value_type']):
    python_type = dict

    def parse(self, value):
        python_type = self.python_type

        if isinstance(value, python_type):
            value = value.items()
        elif isinstance(value, (str, bytes)):
            value = value.split()
            value = (pair.split('=', 1) for pair in value)
        elif isinstance(value, collections.iterable):
            pass
        else:
            raise TypeError('Expected a dict of {} -> {}, got {}'.format(self.key_type, self.value_type, type(value)))

        key_converter = lambda key: parse(key, self.key_type)
        value_converter = lambda value: parse(value, self.value_type)
        value = python_type((key_converter(k), value_converter(v)) for k, v in value)
        return value