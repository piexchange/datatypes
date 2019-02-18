
import io

from .type import Type

__all__ = ['File']


class File(Type):
    python_type = io.IOBase

    @staticmethod
    def convert(value):
        if isinstance(value, str):
            return open(value, encoding='utf-8')

        raise TypeError('Expected a file, got {}'.format(type(value)))
