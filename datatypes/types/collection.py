
import collections.abc

from .type import Type
from .generics import GenericMeta
from ..util import parse

__all__ = ['Collection']


class CollectionMeta(GenericMeta):
    def __new__(mcs, name, bases, attrs, subtype_names=['item_type']):
        return super().__new__(mcs, name, bases, attrs, subtype_names)

    def __init__(mcs, name, bases, attrs, subtype_names=['item_type']):
        return super().__init__(name, bases, attrs, subtype_names)

    def __instancecheck__(cls, instance):
        if not isinstance(instance, cls.python_type):
            return False

        first_subtype_name = cls._subtype_names[0]
        if not hasattr(cls, first_subtype_name):
            return True

        first_subtype = getattr(cls, first_subtype_name)
        return all(isinstance(val, first_subtype) for val in instance)


class Collection(Type, metaclass=CollectionMeta):
    python_type = collections.abc.Collection

    @classmethod
    def parse(cls, value):
        if isinstance(value, (str, bytes)):
            value = [val.strip() for val in value.split(',')]
        elif not isinstance(value, collections.abc.Iterable):
            raise TypeError('Expected an iterable, got a {}'.format(type(value).__name__))

        if hasattr(cls, 'item_type'):
            value = (parse(v, cls.item_type) for v in value)

        return cls.python_type(value)
