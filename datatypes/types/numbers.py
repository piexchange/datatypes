
from .type import Type

__all__ = ['Integer', 'NaturalNumber']


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


class NaturalNumber(Integer):
    @classmethod
    def parse(cls, value):
        value = super().parse(value)

        if value >= 0:
            return value

        raise ValueError('Expected a natural number, got {}'.format(value))
