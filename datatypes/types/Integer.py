
from ..Type import Type


class Integer(Type):
    _python_type = int

    @classmethod
    def parse(cls, value):
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                raise TypeError('Expected an integer number, got {!r}'.format(value))

        raise TypeError('Expected an integer number, got {}'.format(type(value)))
