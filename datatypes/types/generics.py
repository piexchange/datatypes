
from .type import *

__all__ = ['GenericMeta', 'QualifiedGenericMeta']


class GenericMeta(TypeMeta):
    def __new__(mcs, name, bases, attrs, subtype_names):
        return super().__new__(mcs, name, bases, attrs)

    def __init__(cls, name, bases, attrs, subtype_names):
        super().__init__(name, bases, attrs)

        cls._subtype_names = subtype_names
        cls._class_for_subtype = {}

    def __getitem__(cls, subtypes):
        if not isinstance(subtypes, tuple):
            subtypes = (subtypes,)

        for subtype in subtypes:
            if not isinstance(subtype, type):
                raise TypeError('subtypes must be types, not {}'.format(subtype))

        if subtypes in cls._class_for_subtype:
            return cls._class_for_subtype[subtypes]

        metacls = type('Specialized{}Meta'.format(cls.__name__), (QualifiedGenericMeta, type(cls)), {})
        name = '{}[{}]'.format(cls.__name__, ', '.join(subtype.__name__ for subtype in subtypes))
        bases = (cls,)
        attrs = {'_base': cls}

        subcls = metacls(name, bases, attrs)
        for subtype, subtype_name in zip(subtypes, cls._subtype_names):
            setattr(subcls, subtype_name, subtype)

        cls._class_for_subtype[subtypes] = subcls
        return subcls


class QualifiedGenericMeta(GenericMeta):
    def __new__(mcs, *args, **kwargs):
        # skip GenericMeta.__new__
        return super(GenericMeta, mcs).__new__(mcs, *args, **kwargs)

    def __init__(cls, *args, **kwargs):
        # skip GenericMeta.__init__
        super(GenericMeta, cls).__init__(*args, **kwargs)

    def __getitem__(cls, subtypes):
        raise TypeError("{} is not a generic class".format(cls.__name__))

    def _list_subtypes(cls):
        return tuple(getattr(cls, attr) for attr in cls._subtype_names)


# class Generic(Type, metaclass=GenericMeta):
#     pass
