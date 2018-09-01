
__all__ = ['Type', 'TypeMeta']


class TypeMeta(type):
    pass


class Type(metaclass=TypeMeta):
    @classmethod
    def is_a(cls, type_):
        return issubclass(cls, type_)

    @classmethod
    def parse(cls, value):
        raise NotImplementedError
