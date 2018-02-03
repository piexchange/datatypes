
from datetime import datetime

from datatypes.Type import Type


class Datetime(Type):
    def __init__(self, format=None, timezone=None):
        self.format = format
        self.timezone = timezone

    def convert(self, value):
        if isinstance(value, str):
            return datetime.strptime(value, self.format)

        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value, self.timezone)

        raise TypeError("Expected a date and time, got {}".format(type(value)))
