
from .unit import *


class Time(metaclass=CategoryMeta):
    pass


class Weeks(metaclass=Time):
    _abbr = 'w'
    _value = 60 * 60 * 24 * 7


class Days(metaclass=Time):
    _abbr = 'd'
    _value = 60 * 60 * 24


class Hours(metaclass=Time):
    _abbr = 'h'
    _value = 60 * 60


class Minutes(metaclass=Time):
    _abbr = 'min'
    _value = 60


class Seconds(metaclass=Time):
    _abbr = 'sec'
    _value = 1
