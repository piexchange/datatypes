
from .type import Type


class Boolean(Type):
    python_type = bool

    @staticmethod
    def parse(value):
        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            val = value.lower()
            if val in {'yes', 'y', 'on', 'true'}:
                return True
            if val in {'no', 'n', 'off', 'false'}:
                return False
        else:
            if value in {1}:
                return True
            if value in {0}:
                return False

        raise TypeError('Expected a boolean, got {}'.format(value))
