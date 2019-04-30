
__all__ = ['Type', 'TypeMeta']


class TypeMeta(type):
    def __str__(self):
        return self.__name__

    # def __subclasscheck__(cls, subcls):
    #     return issubclass(subcls, cls.python_type) or super().__subclasscheck__(subcls)

    def __instancecheck__(cls, instance):
        return isinstance(instance, cls.python_type)

    @property
    def python_type(cls):
        try:
            return vars(cls)['python_type']
        except KeyError:
            raise AttributeError('{} has no equivalent python type'.format(cls.__qualname__)) from None

    @property
    def typing_type(cls):
        try:
            return vars(cls)['typing_type']
        except KeyError:
            raise AttributeError('{} has no equivalent typing type'.format(cls.__qualname__)) from None


class Type(metaclass=TypeMeta):
    def __new__(cls, *args, **kwargs):
        raise TypeError('Types cannot be instantiated')

    @classmethod
    def is_a(cls, type_):
        from ..type_checks import is_subtype

        return is_subtype(cls, type_)

    @classmethod
    def parse(cls, value):
        from ..type_checks import is_instance

        if is_instance(value, cls):
            return value

        raise TypeError('Expected a {}, got a {}'.format(cls.python_type.__name__, type(value).__name__))
