
import collections.abc

from .type import Type
from .generics import GenericMeta
from ..util import parse


class CollectionMeta(GenericMeta):
    def __instancecheck__(cls, instance):
        if not isinstance(instance, cls.python_type):
            return False

        if not hasattr(cls, 'subtype'):
            return True

        return all(isinstance(val, cls.subtype) for val in instance)


class Collection(Type, metaclass=CollectionMeta):
    @classmethod
    def parse(cls, value):
        if isinstance(value, (str, bytes)):
            value = [val.strip() for val in value.split(',')]
        elif not isinstance(value, collections.abc.Iterable):
            raise TypeError('Expected an iterable, got a {}'.format(type(value).__name__))

        if hasattr(cls, 'subtype'):
            value = (parse(v, cls.subtype) for v in value)

        return cls.python_type(value)
