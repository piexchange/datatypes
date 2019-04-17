
import typing

from .type import Type

__all__ = ['Any']


class Any(Type):
    typing_type = typing.Any

    @staticmethod
    def parse(value):
        return value
