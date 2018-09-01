
from datatypes.type import Type


class Any(Type):
    @staticmethod
    def parse(value):
        return value
