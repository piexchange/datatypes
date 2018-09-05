
from .type import *

__all__ = ['GenericMeta', 'Generic']


class GenericMeta(TypeMeta):
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
            metacls = type(cls)
            name = '{}[{}]'.format(cls.__name__, subtype.__name__)
            bases = (cls,)
            attrs = {}

            subcls = metacls(name, bases, attrs, subtype=subtype)
            cls._class_for_subtype[subtype] = subcls

        return cls._class_for_subtype[subtype]


# class Generic(Type, metaclass=GenericMeta):
#     pass
