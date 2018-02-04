
import collections

from .Collection import Collection
from ..util import Converter


class List(Collection):
    _python_type = list

    def parse(self, value):
        if isinstance(value, list):
            pass
        elif isinstance(value, (str, bytes)):
            value = value.split()
        elif isinstance(value, collections.iterable):
            value = list(value)
        else:
            raise TypeError('Expected a list of {}, got {}'.format(self.item_type, type(value)))

        converter = Converter(self.item_type)
        value = [converter.convert(v) for v in value]
        return value
