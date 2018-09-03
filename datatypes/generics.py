
from .type import *

__all__ = ['GenericMeta', 'Generic']


class GenericMeta(TypeMeta):
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        
        cls.__subclasses = {}
        
        return cls
    
    def __getitem__(cls, subtype):
        assert isinstance(subtype, type), subtype
        
        if cls.__bases__[0] is __class__:
            raise TypeError('{} is not a generic'.format(cls))
        
        if subtype not in cls.__subclasses:
            metacls = __class__
            name = '{}[{}]'.format(cls.__name__, subtype.__name__)
            bases = (cls,)
            attrs = {}
            subcls = metacls(name, bases, attrs)
            
            cls.__subclasses[subtype] = subcls
            
        return cls.__subclasses[subtype]


class Generic(Type, metaclass=GenericMeta):
    pass
