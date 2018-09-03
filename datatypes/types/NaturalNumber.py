
from .Integer import Integer


class NaturalNumber(Integer):
    @classmethod
    def parse(cls, value):
        value = super().parse(value)
            
        if value >= 0:
            return value

        raise ValueError('Expected a natural number, got {}'.format(value))
