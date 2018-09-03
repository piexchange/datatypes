
import collections.abc

from ..type import *
from ..util import parse


class CollectionMeta(TypeMeta):
    def __new__(mcs, name, bases, attrs, subtype=None):
        return super().__new__(mcs, name, bases, attrs)

    def __init__(cls, name, bases, attrs, subtype=None):
        super().__init__(name, bases, attrs)

        if subtype is None:
            cls._class_for_subtype = {}
        else:
            cls.subtype = subtype

    def __getitem__(cls, subtype):
        if not isinstance(subtype, type):
            raise TypeError('subtype must be a type, not {}'.format(subtype))

        if hasattr(cls, 'subtype'):
            raise TypeError('{} is not a generic class'.format(cls))

        if subtype not in cls._class_for_subtype:
            metacls = __class__
            name = '{}[{}]'.format(cls.__name__, subtype.__name__)
            bases = (cls,)
            attrs = {}

            subcls = metacls(name, bases, attrs, subtype=subtype)
            cls._class_for_subtype[subtype] = subcls

        return cls._class_for_subtype[subtype]

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
