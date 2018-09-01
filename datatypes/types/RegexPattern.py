
import re

from ..type import Type


class RegexPattern(Type):
    @staticmethod
    def parse(value):
        if isinstance(value, str):
            return re.compile(value)

        if isinstance(value, re.Pattern):
            return value

        raise TypeError('Expected a string, got {}'.format(type(value)))
