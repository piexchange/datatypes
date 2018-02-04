
from pathlib import Path

from ..Type import Type


class FilePath(Type):
    _python_type = Path

    @classmethod
    def parse(cls, value):
        if isinstance(value, cls.python_type):
            return value
        elif isinstance(value, str):
            return Path(value)

        raise TypeError('Expected a file path, got {}'.format(type(value)))


class OpenFilePath(FilePath):
    pass


class SaveFilePath(FilePath):
    pass
