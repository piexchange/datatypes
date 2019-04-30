
import typing

from .type import Type, TypeMeta

__all__ = ['Any']


class AnyMeta(TypeMeta):
    def __instancecheck__(cls, instance):
        return True


class Any(Type, metaclass=AnyMeta):
    typing_type = typing.Any

    @staticmethod
    def parse(value):
        return value
