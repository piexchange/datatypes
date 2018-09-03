
from .Unit import Unit


class ByteUnit(metaclass=Unit):
    pass


class terabytes(ByteUnit):
    _abbr = 'TB'
    _value = 1000 ** 4


class gigabytes(ByteUnit):
    _abbr = 'GB'
    _value = 1000 ** 3


class megabytes(ByteUnit):
    _abbr = 'MB'
    _value = 1000 ** 2


class kilobytes(ByteUnit):
    _abbr = 'KB'
    _value = 1000


class bytes(ByteUnit):
    _abbr = 'B'
    _value = 1
