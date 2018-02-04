
import collections

from .Collection import Collection
from ..util import Converter


class Set(Collection):
    _python_type = set

    def parse(self, value):
        python_type = self.python_type

        if isinstance(value, python_type):
            pass
        elif isinstance(value, (str, bytes)):
            value = value.split()
        elif isinstance(value, collections.iterable):
            pass
        else:
            raise TypeError('Expected a set of {}, got {}'.format(self.item_type, type(value)))

        converter = Converter(self.item_type)
        value = python_type(converter.convert(v) for v in value)
        return value