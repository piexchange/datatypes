
from .type import Type

__all__ = ['Any']


class Any(Type):
    @staticmethod
    def parse(value):
        return value
