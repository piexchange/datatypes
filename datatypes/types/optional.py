
from .type import Type
from .generics import GenericMeta
from ..parse import parse

__all__ = ['Optional']


class OptionalMeta(GenericMeta):
    def __instancecheck__(cls, instance):
        if not hasattr(cls, 'subtype'):
            return True

        return instance is None or isinstance(instance, cls.subtype)


class Optional(Type, metaclass=OptionalMeta, subtype_names=['subtype']):
    @classmethod
    def parse(cls, value):
        if not hasattr(cls, 'subtype'):
            return value

        if value is None:
            return value

        return parse(value, cls.subtype)
