
__all__ = ['Type']


class _TypeMeta(type):
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)

        if name != 'Type':
            setattr(Type, name, cls)

        return cls


class Type(metaclass=_TypeMeta):
    @classmethod
    def is_a(cls, type_):
        if isinstance(type_, type):
            return issubclass(cls, type_)

        return issubclass(cls, type_.__class__)

    @classmethod
    def convert(cls, value):
        raise NotImplementedError
