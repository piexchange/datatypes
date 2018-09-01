
import os

from ..type import Type


class FilePath(Type):
    @staticmethod
    def convert(value):
        if isinstance(value, (str, os.Pathlike)):
            return value

        raise TypeError('Expected a file path, got {}'.format(type(value)))


class OpenFilePath(FilePath):
    pass


class SaveFilePath(FilePath):
    pass
