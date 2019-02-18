
import re

from .type import Type

__all__ = ['RegexPattern']


class RegexPattern(Type):
    python_type = re.Pattern if hasattr(re, 'Pattern') else re._pattern_type

    @classmethod
    def parse(cls, value):
        if isinstance(value, (str, bytes)):
            return re.compile(value)

        if isinstance(value, cls.python_type):
            return value

        raise TypeError('Expected a regex pattern, got {}'.format(type(value).__name__))
