
from datatypes.Type import Type


class FilePath(Type):
    @staticmethod
    def convert(value):
        if isinstance(value, str):
            return value

        raise TypeError('Expected a file path, got {}'.format(type(value)))


class OpenFilePath(FilePath):
    pass


class SaveFilePath(FilePath):
    pass
