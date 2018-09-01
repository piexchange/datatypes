
from datatypes.type import Type


class Choice(Type):  # FIXME: This is not a data type.
    def __init__(self, *choices):
        self.choices = set(choices)

    def convert(self, value):
        if value in self.choices:
            return value

        raise TypeError('Expected one of {}, got {}'.format(self.choices, value))
