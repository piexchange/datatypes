
from ..Type import Type


class Choice(Type):
    def __init__(self, *choices):
        self.choices = set(choices)

    def parse(self, value):
        # FIXME: try to PARSE the value into a valid choice
        if value in self.choices:
            return value

        raise TypeError('Expected one of {}, got {}'.format(self.choices, value))
