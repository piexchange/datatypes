
from .unit import *


class Distance(metaclass=CategoryMeta):
    pass


class Kilometers(metaclass=Distance):
    _abbr = 'km'
    _value = 1000


class Meters(metaclass=Distance):
    _abbr = 'm'
    _value = 1


class Decimeters(metaclass=Distance):
    _abbr = 'dm'
    _value = 0.1


class Centimeters(metaclass=Distance):
    _abbr = 'cm'
    _value = 0.01


class Millimeters(metaclass=Distance):
    _abbr = 'mm'
    _value = 0.001


class Micrometers(metaclass=Distance):
    _abbr = 'mm'
    _value = 0.000001


class Nanometers(metaclass=Distance):
    _abbr = 'nm'
    _value = 0.000000001
