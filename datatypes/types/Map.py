
import collections

from .Collection import Collection


class Map(Collection):
    def __init__(self, key_type, value_type):
        super().__init__(key_type)

        self.key_type = key_type
        self.value_type = value_type

    def convert(self, value):
        if isinstance(value, dict):
            pass
        elif isinstance(value, (str, bytes)):
            value = value.split()
            value = dict(pair.split('=', 1) for pair in value)
        elif isinstance(value, collections.iterable):
            value = dict(value)
        else:
            raise TypeError('Expected a dict of {} -> {}, got {}'.format(self.key_type, self.value_type, type(value)))

        key_converter = Converter(self.key_type)
        value_converter = Converter(self.value_type)
        value = {key_converter.convert(k): value_converter.convert(v) for k, v in value.items()}
        return value
