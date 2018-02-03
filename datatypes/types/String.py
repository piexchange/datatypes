
from datatypes.Type import Type


class String(Type):
    @staticmethod
    def convert(value):
        if isinstance(value, str):
            return value

        raise TypeError('Expected a string, got {}'.format(type(value)))
