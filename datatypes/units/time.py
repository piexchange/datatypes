
from .Unit import Unit


class TimeUnit(Unit, is_category=True):
    pass


class hours(TimeUnit):
    _abbr = 'h'
    _value = 60 * 60


class minutes(TimeUnit):
    _abbr = 'min'
    _value = 60


class seconds(TimeUnit):
    _abbr = 'sec'
    _value = 1
