
from ..Type import Type


class String(Type):
    _python_type = str
    
    @classmethod
    def convert(cls, value):
        if isinstance(value, cls.python_type):
            return value

        raise TypeError('Expected a string, got {}'.format(type(value)))
