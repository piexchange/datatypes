
__all__ = ['Type', 'TypeMeta']


class TypeMeta(type):
    def __str__(self):
        return self.__name__

    # def __subclasscheck__(cls, subcls):
    #     return issubclass(subcls, cls.python_type) or super().__subclasscheck__(subcls)

    def __instancecheck__(cls, instance):
        return isinstance(instance, cls.python_type)


class Type(metaclass=TypeMeta):
    def __new__(cls, *args, **kwargs):
        raise TypeError('Types cannot be instantiated')

    @classmethod
    def is_a(cls, type_):
        return issubclass(cls, type_)

    @classmethod
    def parse(cls, value):
        if isinstance(value, cls):
            return value

        raise TypeError('Expected a {}, got a {}'.format(cls.python_type.__name__, type(value).__name__))
