
from datatypes.Type import Type


class Boolean(Type):
    @staticmethod
    def convert(value):
        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            val = value.lower()
            if val in {'yes', 'y'}:
                return True
            if val in {'no', 'n'}:
                return False
        else:
            if value in {1}:
                return True
            if value in {0}:
                return False

        raise TypeError('Expected a boolean, got {}'.format(value))
