
from ..generics import Generic
from ..util import parse


class Collection(Generic):
    collection_type = None
    
    @classmethod
    def parse(cls, value):
        try:
            iter(value)
        except TypeError:
            raise TypeError('Expected an iterable, got {}'.format(value))
        
        itr = (parse(val, cls.subtype) for val in value)
        return cls.collection_type(itr)
