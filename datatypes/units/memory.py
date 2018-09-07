
from .unit import *


class Memory(metaclass=CategoryMeta):
    pass


# BINARY
class BinaryBytes(Memory):
    pass


class Tebibytes(metaclass=BinaryBytes):
    _abbr = 'TB'
    _value = 1024 ** 4


class Gibibytes(metaclass=BinaryBytes):
    _abbr = 'GB'
    _value = 1024 ** 3


class Mebibytes(metaclass=BinaryBytes):
    _abbr = 'MB'
    _value = 1024 ** 2


class Kibibytes(metaclass=BinaryBytes):
    _abbr = 'KB'
    _value = 1024


class Bytes(metaclass=BinaryBytes):
    _abbr = 'B'
    _value = 1


# DECIMAL
class DecimalBytes(Memory):
    pass


class Terabytes(metaclass=DecimalBytes):
    _abbr = 'TB'
    _value = 1000 ** 4


class Gigabytes(metaclass=DecimalBytes):
    _abbr = 'GB'
    _value = 1000 ** 3


class Megabytes(metaclass=DecimalBytes):
    _abbr = 'MB'
    _value = 1000 ** 2


class Kilobytes(metaclass=DecimalBytes):
    _abbr = 'KB'
    _value = 1000


class Bytes(metaclass=DecimalBytes):
    _abbr = 'B'
    _value = 1

