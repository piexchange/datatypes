
from ..Type import Type


class Collection(Type):
    def __init__(self, item_type):
        super().__init__()

        self.item_type = item_type
