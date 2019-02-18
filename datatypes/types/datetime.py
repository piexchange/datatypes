
from datetime import datetime

from .type import Type

__all__ = ['Datetime']


class Datetime(Type):
    _python_type = datetime

    def __init__(self, format=None, timezone=None):
        self.format = format
        self.timezone = timezone

    def parse(self, value):
        if isinstance(value, str):
            return datetime.strptime(value, self.format)

        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value, self.timezone)

        raise TypeError("Expected a date and time, got {}".format(type(value)))
