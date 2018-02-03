
import collections

from .Collection import Collection
from ..util import Converter


class Set(Collection):
    def convert(self, value):
        if isinstance(value, set):
            pass
        elif isinstance(value, (str, bytes)):
            value = value.split()
        elif isinstance(value, collections.iterable):
            value = list(value)
        else:
            raise TypeError('Expected a set of {}, got {}'.format(self.item_type, type(value)))

        converter = Converter(self.item_type)
        value = set(converter.convert(v) for v in value)
        return value