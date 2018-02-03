
from datatypes.Type import Type


class NaturalNumber(Type):
    @staticmethod
    def convert(value):
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                raise TypeError('Expected a natural number, got {!r}'.format(value))
            
        if isinstance(value, int):
            if value <= 0:
                raise TypeError('Expected a natural number, got {}'.format(value))
            return value
        
        raise TypeError('Expected a natural number, got {}'.format(type(value)))