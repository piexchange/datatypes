
import typing

from datatypes.types import Type
from datatypes.types.generics import GenericMeta, QualifiedGenericMeta
from datatypes import types as dtypes

__all__ = ['get_python_type', 'is_generic', 'is_base_generic', 'is_qualified_generic', 'get_base_generic',
           'get_subtypes']


if hasattr(typing, '_GenericAlias'):
    # python 3.7
    def _is_generic(cls):
        if isinstance(cls, typing._GenericAlias):
            return True

        if isinstance(cls, typing._SpecialForm):
            return cls not in {typing.Any}

        return False


    def _is_base_generic(cls):
        if isinstance(cls, typing._GenericAlias):
            if cls.__origin__ in {typing.Generic, typing._Protocol}:
                return False

            if isinstance(cls, typing._VariadicGenericAlias):
                return True

            return len(cls.__parameters__) > 0

        if isinstance(cls, typing._SpecialForm):
            return cls._name in {'ClassVar', 'Union', 'Optional'}

        return False


    def _get_base_generic(cls):
        # subclasses of Generic will have their _name set to None, but
        # their __origin__ will point to the base generic
        if cls._name is None:
            return cls.__origin__
        else:
            return getattr(typing, cls._name)


    def _get_python_type(cls):
        """
        Like `python_type`, but only works with `typing` classes.
        """
        return cls.__origin__


    def _get_name(cls):
        try:
            return cls._name
        except AttributeError:
            return cls.__name__
else:
    # python <3.7
    if hasattr(typing, '_Union'):
        # python 3.6
        def _is_generic(cls):
            if isinstance(cls, (typing.GenericMeta, typing._Union, typing._Optional, typing._ClassVar)):
                return True

            return False


        def _is_base_generic(cls):
            if isinstance(cls, (typing.GenericMeta, typing._Union)):
                return cls.__args__ in {None, ()}

            if isinstance(cls, typing._Optional):
                return True

            return False
    else:
        # python 3.5
        def _is_generic(cls):
            if isinstance(cls, (typing.GenericMeta, typing.UnionMeta, typing.OptionalMeta, typing.CallableMeta, typing.TupleMeta)):
                return True

            return False


        def _is_base_generic(cls):
            if isinstance(cls, typing.GenericMeta):
                return all(isinstance(arg, typing.TypeVar) for arg in cls.__parameters__)

            if isinstance(cls, typing.UnionMeta):
                return cls.__union_params__ is None

            if isinstance(cls, typing.TupleMeta):
                return cls.__tuple_params__ is None

            if isinstance(cls, typing.CallableMeta):
                return cls.__args__ is None

            if isinstance(cls, typing.OptionalMeta):
                return True

            return False


    def _get_base_generic(cls):
        try:
            return cls.__origin__
        except AttributeError:
            pass

        name = type(cls).__name__
        if not name.endswith('Meta'):
            raise NotImplementedError("Cannot determine base of {}".format(cls))

        name = name[:-4]
        try:
            return getattr(typing, name)
        except AttributeError:
            raise NotImplementedError("Cannot determine base of {}".format(cls))


    def _get_python_type(cls):
        """
        Like `python_type`, but only works with `typing` classes.
        """
        # Many classes actually reference their corresponding abstract base class from the abc module
        # instead of their builtin variant (i.e. typing.List references MutableSequence instead of list).
        # We're interested in the builtin class (if any), so we'll traverse the MRO and look for it there.
        for typ in cls.mro():
            if typ.__module__ == 'builtins' and typ is not object:
                return typ

        try:
            return cls.__extra__
        except AttributeError:
            pass

        if is_qualified_generic(cls):
            cls = get_base_generic(cls)

        if cls is typing.Tuple:
            return tuple

        raise NotImplementedError("Cannot determine python type of {}".format(cls))


    def _get_name(cls):
        try:
            return cls.__name__
        except AttributeError:
            return type(cls).__name__[1:]


if hasattr(typing.List, '__args__'):
    # python 3.6+
    def _get_subtypes(cls):
        subtypes = cls.__args__

        if get_base_generic(cls) is typing.Callable:
            if len(subtypes) != 2 or subtypes[0] is not ...:
                subtypes = (subtypes[:-1], subtypes[-1])

        return subtypes
else:
    # python 3.5
    def _get_subtypes(cls):
        if isinstance(cls, typing.CallableMeta):
            if cls.__args__ is None:
                return ()

            return cls.__args__, cls.__result__

        for name in ['__parameters__', '__union_params__', '__tuple_params__']:
            try:
                subtypes = getattr(cls, name)
                break
            except AttributeError:
                pass
        else:
            raise NotImplementedError("Cannot extract subtypes from {}".format(cls))

        subtypes = [typ for typ in subtypes if not isinstance(typ, typing.TypeVar)]
        return subtypes


def _is_protocol(cls):
    return isinstance(cls, typing._ProtocolMeta)


def is_generic(cls):
    """
    Detects any kind of generic, for example `List` or `List[int]`. This includes "special" types like
    Union and Tuple - anything that's subscriptable, basically.
    """
    if isinstance(cls, GenericMeta):
        return True

    return _is_generic(cls)


def is_base_generic(cls):
    """
    Detects generic base classes, for example `List` (but not `List[int]`)
    """
    if isinstance(cls, GenericMeta):
        return not isinstance(cls, QualifiedGenericMeta)

    return _is_base_generic(cls)


def is_qualified_generic(cls):
    """
    Detects generics with arguments, for example `List[int]` (but not `List`)
    """
    return is_generic(cls) and not is_base_generic(cls)


def get_base_generic(cls):
    if not is_qualified_generic(cls):
        raise TypeError('{} is not a qualified Generic and thus has no base'.format(cls))

    if isinstance(cls, GenericMeta):
        return cls._base

    return _get_base_generic(cls)


def get_subtypes(cls):
    if isinstance(cls, QualifiedGenericMeta):
        return cls._list_subtypes()

    return _get_subtypes(cls)


def get_python_type(annotation):
    """
    Given a type annotation or a class as input, returns the corresponding python class.

    Examples:

    ::
        >>> get_python_type(typing.Dict)
        <class 'dict'>
        >>> get_python_type(typing.List[int])
        <class 'list'>
        >>> get_python_type(int)
        <class 'int'>
    """
    try:
        mro = annotation.mro()
    except AttributeError:
        # if it doesn't have an mro method, it must be a weird typing object
        return _get_python_type(annotation)

    if Type in mro:
        try:
            return annotation.python_type
        except AttributeError:
            raise ValueError("There is no python equivalent of {}".format(annotation))
    elif annotation.__module__ == 'typing':
        return _get_python_type(annotation)
    else:
        return annotation
