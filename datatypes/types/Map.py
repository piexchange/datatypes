
import collections

from .Collection import Collection
from ..util import parse


class Map(Collection):
    _python_type = dict

    def __init__(self, key_type, value_type):
        super().__init__(key_type)

        self.key_type = key_type
        self.value_type = value_type

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