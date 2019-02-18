
import sys

from .type import Type

__all__ = ['String']


class String(Type):
    python_type = str if sys.version_info.major >= 3 else unicode
    
    @classmethod
    def parse(cls, value):
        if isinstance(value, cls.python_type):
            return value
        elif isinstance(value, bytes):
            try:
                return value.decode()
            except UnicodeDecodeError:
                raise ValueError('Failed to decode non-utf8 byte sequence to a string')
        else:
            return str(value)

        # raise TypeError('Expected a string, got {}'.format(type(value)))
