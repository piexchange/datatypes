
from datatypes.Type import Type


class Any(Type):
    @staticmethod
    def convert(value):
        return value
