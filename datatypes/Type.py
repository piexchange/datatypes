
__all__ = ['Type']


class _TypeMeta(type):
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)

        if name != 'Type':
            setattr(Type, name, cls)

        return cls

    @property
    def python_type(cls):
        return getattr(cls, '_python_type', None)


class Type(metaclass=_TypeMeta):
    @classmethod
    def is_a(cls, type_):
        if isinstance(type_, type):
            return issubclass(cls, type_)

        return issubclass(cls, type_.__class__)

    @property
    def python_type(self):
        return type(self).python_type

    @classmethod
    def parse(cls, value):
        raise NotImplementedError
