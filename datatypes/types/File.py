
import io

from datatypes.Type import Type


class File(Type):
    _python_type = io.IOBase

    @staticmethod
    def convert(value):
        if isinstance(value, str):
            return open(value, encoding='utf-8')

        raise TypeError('Expected a file, got {}'.format(type(value)))
