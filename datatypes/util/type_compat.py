
import typing

from ..types import Type
from .. import types as dtypes

__all__ = ['is_instance', 'is_subtype', 'python_type', 'typing_to_datatype']


def _instancecheck_iterable(iterable, type_args):
    if len(type_args) != 1:
        raise TypeError("Generic iterables must have exactly 1 type argument; found {}".format(type_args))

    type_ = type_args[0]
    return all(is_instance(val, type_) for val in iterable)


def _instancecheck_mapping(mapping, type_args):
    return _instancecheck_itemsview(mapping.items(), type_args)


def _instancecheck_itemsview(itemsview, type_args):
    if len(type_args) != 2:
        raise TypeError("Generic mappings must have exactly 2 type arguments; found {}".format(type_args))

    key_type, value_type = type_args
    return all(is_instance(key, key_type) and is_instance(val, value_type) for key, val in itemsview)


def _instancecheck_tuple(tup, type_args):
    if len(tup) != len(type_args):
        return False

    return all(is_instance(val, type_) for val, type_ in zip(tup, type_args))


_ORIGIN_TYPE_CHECKERS = {}
for class_path, check_func in {
                        # iterables
                        'typing.Container': _instancecheck_iterable,
                        'typing.Collection': _instancecheck_iterable,
                        'typing.AbstractSet': _instancecheck_iterable,
                        'typing.MutableSet': _instancecheck_iterable,
                        'typing.Sequence': _instancecheck_iterable,
                        'typing.MutableSequence': _instancecheck_iterable,
                        'typing.ByteString': _instancecheck_iterable,
                        'typing.Deque': _instancecheck_iterable,
                        'typing.List': _instancecheck_iterable,
                        'typing.Set': _instancecheck_iterable,
                        'typing.FrozenSet': _instancecheck_iterable,
                        'typing.KeysView': _instancecheck_iterable,
                        'typing.ValuesView': _instancecheck_iterable,
                        'typing.AsyncIterable': _instancecheck_iterable,

                        # mappings
                        'typing.Mapping': _instancecheck_mapping,
                        'typing.MutableMapping': _instancecheck_mapping,
                        'typing.MappingView': _instancecheck_mapping,
                        'typing.ItemsView': _instancecheck_itemsview,
                        'typing.Dict': _instancecheck_mapping,
                        'typing.DefaultDict': _instancecheck_mapping,
                        'typing.Counter': _instancecheck_mapping,
                        'typing.ChainMap': _instancecheck_mapping,

                        # other
                        'typing.Tuple': _instancecheck_tuple,
                    }.items():
    try:
        cls = eval(class_path)
    except AttributeError:
        continue

    _ORIGIN_TYPE_CHECKERS[cls] = check_func


# typing module compatibility functions
def _is_generic(cls):
    """
    Detects any kind of generic, for example `List` or `List[int]`
    """
    # check if the class inherits from any `typing` class
    if cls.__module__ != 'typing':
        if not any(c.__module__ == 'typing' for c in cls.mro()):
            return False

    # only generics have a non-empty __parameters__ tuple
    params = getattr(cls, '__parameters__', ())
    if params:
        return True

    # if the __parameters__ tuple was empty, the only way
    # this could be a generic is if it has already received
    # its type arguments
    return bool(getattr(cls, '__args__', ()))


def _is_base_generic(cls):
    """
    Detects generic base classes, for example `List` (but not `List[int]`)
    """
    return _is_generic(cls) and bool(cls.__parameters__)


def _is_specialized_generic(cls):
    """
    Detects generics with arguments, for example `List[int]` (but not `List`)
    """
    return _is_generic(cls) and not cls.__parameters__


def _get_base_generic(cls):
    # python 3.7
    if hasattr(cls, '_name'):
        # subclasses of Generic will have their _name set to None, but
        # their __origin__ will point to the base generic
        if cls._name is None:
            return cls.__origin__
        else:
            return getattr(typing, cls._name)

    # python 3.6 and older
    return cls.__origin__


def _get_subtypes(cls):
    return cls.__args__


def _get_python_type(cls):
    # python 3.6 and older
    if hasattr(cls, '__extra__'):
        return cls.__extra__
    # python 3.7
    else:
        return cls.__origin__
# end of typing compatibility


def is_instance(obj, type_):
    if _is_base_generic(type_):
        python_type = _get_python_type(type_)
        return isinstance(obj, python_type)

    if _is_specialized_generic(type_):
        python_type = _get_python_type(type_)
        if not isinstance(obj, python_type):
            return False

        base = _get_base_generic(type_)
        try:
            validator = _ORIGIN_TYPE_CHECKERS[base]
        except KeyError:
            raise NotImplementedError("Cannot perform isinstance check for type {}".format(type_))

        type_args = type_.__args__
        return validator(obj, type_args)

    return isinstance(obj, type_)


def is_subtype(cls, type_):
    if _is_base_generic(type_):
        python_type = _get_python_type(type_)
        return issubclass(cls, python_type)

    if _is_specialized_generic(type_):
        container_type = _get_python_type(type_)

        if _is_specialized_generic(cls):
            container_subtypes = _get_subtypes(type_)
            subtypes = _get_subtypes(cls)

            type_pairs = zip(subtypes, container_subtypes)
            if not all(is_subtype(sub, sup) for sub, sup in type_pairs):
                return False

        return issubclass(cls, container_type)

    return issubclass(cls, type_)


def python_type(annotation):
    """
    Given a type annotation or a class as input, returns the corresponding python class.

    Examples:

    ::
        >>> python_type(typing.Dict)
        <class 'dict'>
        >>> python_type(typing.List[int])
        <class 'list'>
        >>> python_type(int)
        <class 'int'>
    """
    try:
        mro = annotation.mro()
    except AttributeError:
        # if it doesn't have an mro method, it must be a weird typing object
        return _get_python_type(annotation)

    if Type in mro:
        return annotation.python_type
    elif annotation.__module__ == 'typing':
        return _get_python_type(annotation)
    else:
        return annotation


def typing_to_datatype(typing_annotation):
    """
    Given a class or object from the typing module as input, returns the corresponding datatypes class. If the input
    is any other class, it is returned unchanged.
    """
    if _is_generic(typing_annotation):
        python_class = python_type(typing_annotation)

        for cls in vars(dtypes).values():
            if getattr(cls, 'python_type', None) is python_class:
                break
        else:
            raise NotImplementedError("Sorry, there doesn't seem to be a datatypes equivalent of {}".format(typing_annotation))

        subtypes = _get_subtypes(typing_annotation)
        if not subtypes:
            return cls

        subtypes = tuple(typing_to_datatype(subtype) for subtype in subtypes)
        return cls[subtypes]

    return {
        typing.Any: dtypes.Any,
    }.get(typing_annotation, typing_annotation)
