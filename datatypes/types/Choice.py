
from datatypes.Type import Type


class Choice(Type):
    def __init__(self, *choices):
        self.choices = set(choices)

    def convert(self, value):
        if value in self.choices:
            return value

        raise TypeError('Expected one of {}, got {}'.format(self.choices, value))
