
import sys

from .type import Type

__all__ = ['Text']

if sys.version_info.major >= 3:
    TEXT = str
    BYTES = bytes
else:
    TEXT = unicode
    BYTES = str


class Text(Type):
    python_type = TEXT
    
    @classmethod
    def parse(cls, value):
        if isinstance(value, cls.python_type):
            return value
        elif isinstance(value, BYTES):
            try:
                return value.decode('utf-8')
            except UnicodeDecodeError:
                raise ValueError('Failed to decode non-utf8 byte sequence to text')
        else:
            return cls.parse(str(value))

        # raise TypeError('Expected a string, got {}'.format(type(value)))
