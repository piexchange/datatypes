
from datatypes.Type import Type


class Any(Type):
    _python_type = object

    @staticmethod
    def parse(value):
        return value
