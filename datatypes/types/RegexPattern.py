
import re

from datatypes.Type import Type


class RegexPattern(Type):
    @staticmethod
    def convert(value):
        if isinstance(value, str):
            return re.compile(value)

        if isinstance(value, re._pattern_type):
            return value

        raise TypeError('Expected a string, got {}'.format(type(value)))
