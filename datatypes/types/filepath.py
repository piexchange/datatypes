
import os
from pathlib import Path

from .type import Type

__all__ = ['FilePath']


class FilePath(Type):
    python_type = Path

    @classmethod
    def parse(cls, value):
        if isinstance(value, cls.python_type):
            return value
        elif isinstance(value, (str, os.PathLike)):
            return Path(value)

        raise TypeError('Expected a file path, got {}'.format(type(value)))
