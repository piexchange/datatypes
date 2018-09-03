
from ..type import Type


class Integer(Type):
    python_type = int

    @classmethod
    def parse(cls, value):
        try:
            return int(value)
        except ValueError:
            raise ValueError('Expected an integer number, got {!r}'.format(value))
        except TypeError:
            raise TypeError('Expected an integer number, got {!r}'.format(value))
