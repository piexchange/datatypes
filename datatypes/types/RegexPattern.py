
import re

from ..Type import Type


class RegexPattern(Type):
    _python_type = re._pattern_type

    @classmethod
    def parse(cls, value):
        if isinstance(value, (str, bytes)):
            return re.compile(value)

        if isinstance(value, cls.python_type):
            return value

        raise TypeError('Expected a string, got {}'.format(type(value)))
