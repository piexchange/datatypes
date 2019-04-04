
import inspect
import typing

from ..types import Type
from ..types.generics import GenericMeta, QualifiedGenericMeta
from .. import types as dtypes

__all__ = ['is_instance', 'is_subtype', 'python_type', 'typing_to_datatype', 'is_generic', 'is_base_generic',
           'is_qualified_generic']


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


def _instancecheck_callable(value, type_):
    if not callable(value):
        return False

    if is_base_generic(type_):
        return True

    param_types, ret_type = get_subtypes(type_)
    sig = inspect.signature(value)

    missing_annotations = []

    if param_types is not ...:
        if len(param_types) != len(sig.parameters):
            return False

        # FIXME: add support for TypeVars

        # if any of the existing annotations don't match the type, we'll return False.
        # Then, if any annotations are missing, we'll throw an exception.
        for param, expected_type in zip(sig.parameters.values(), param_types):
            param_type = param.annotation
            if param_type is inspect.Parameter.empty:
                missing_annotations.append(param)
                continue

            if not is_subtype(param_type, expected_type):
                return False

    if sig.return_annotation is inspect.Signature.empty:
        missing_annotations.append('return')
    else:
        if not is_subtype(sig.return_annotation, ret_type):
            return False

    if missing_annotations:
        raise ValueError("Missing annotations: {}".format(missing_annotations))

    return True


def _instancecheck_union(value, type_):
    types = get_subtypes(type_)
    return any(is_instance(value, typ) for typ in types)


def _instancecheck_type(value, type_):
    # if it's not a class, return False
    if not isinstance(value, type):
        return False

    if is_base_generic(type_):
        return True

    type_args = get_subtypes(type_)
    if len(type_args) != 1:
        raise TypeError("Type must have exactly 1 type argument; found {}".format(type_args))

    return is_subtype(value, type_args[0])


_SPECIAL_INSTANCE_CHECKERS = {
    'Union': _instancecheck_union,
    'Callable': _instancecheck_callable,
    'Type': _instancecheck_type,
    'Any': lambda v, t: True,
}


def is_generic(cls):
    """
    Detects any kind of generic, for example `List` or `List[int]`. This includes "special" types like
    Union and Tuple - anything that's subscriptable, basically.
    """
    if isinstance(cls, GenericMeta):
        return True

    if isinstance(cls, typing._GenericAlias):
        return True

    if isinstance(cls, typing._SpecialForm):
        return cls not in {typing.Any}

    return False


def is_base_generic(cls):
    """
    Detects generic base classes, for example `List` (but not `List[int]`)
    """
    if isinstance(cls, GenericMeta):
        return not isinstance(cls, QualifiedGenericMeta)

    if isinstance(cls, typing._GenericAlias):
        if cls.__origin__ in {typing.Generic, typing._Protocol}:
            return False

        if isinstance(cls, typing._VariadicGenericAlias):
            return True

        return len(cls.__parameters__) > 0

    if isinstance(cls, typing._SpecialForm):
        return cls._name in {'ClassVar', 'Union', 'Optional'}

    return False


def is_qualified_generic(cls):
    """
    Detects generics with arguments, for example `List[int]` (but not `List`)
    """
    return is_generic(cls) and not is_base_generic(cls)


def get_base_generic(cls):
    if not is_qualified_generic(cls):
        raise TypeError('{} is not a qualified Generic and thus has no base'.format(cls))

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


def get_subtypes(cls):
    if isinstance(cls, QualifiedGenericMeta):
        return cls._list_subtypes()

    subtypes = cls.__args__

    if get_base_generic(cls) is typing.Callable:
        if len(subtypes) != 2 or subtypes[0] is not ...:
            subtypes = (subtypes[:-1], subtypes[-1])

    return subtypes


def _get_python_type(cls):
    """
    Like `python_type`, but only works with `typing` classes.
    """
    # python 3.6 and older
    if hasattr(cls, '__extra__'):
        return cls.__extra__
    # python 3.7
    else:
        return cls.__origin__


def is_instance(obj, type_):
    if type_.__module__ == 'typing':
        if is_qualified_generic(type_):
            base_generic = get_base_generic(type_)
        else:
            base_generic = type_
        name = getattr(base_generic, '_name')

        try:
            validator = _SPECIAL_INSTANCE_CHECKERS[name]
        except KeyError:
            pass
        else:
            return validator(obj, type_)

    if is_base_generic(type_):
        python_type = _get_python_type(type_)
        return isinstance(obj, python_type)

    if is_qualified_generic(type_):
        python_type = _get_python_type(type_)
        if not isinstance(obj, python_type):
            return False

        base = get_base_generic(type_)
        try:
            validator = _ORIGIN_TYPE_CHECKERS[base]
        except KeyError:
            raise NotImplementedError("Cannot perform isinstance check for type {}".format(type_))

        type_args = type_.__args__
        return validator(obj, type_args)

    return isinstance(obj, type_)


def is_subtype(sub_type, super_type):
    if not is_generic(sub_type):
        python_super = python_type(super_type)
        return issubclass(sub_type, python_super)

    # at this point we know `sub_type` is a generic
    python_sub = python_type(sub_type)
    python_super = python_type(super_type)
    if not issubclass(python_sub, python_super):
        return False

    # at this point we know that `sub_type`'s base type is a subtype of `super_type`'s base type.
    # If `super_type` isn't qualified, then there's nothing more to do.
    if not is_generic(super_type) or is_base_generic(super_type):
        return True

    # at this point we know that `super_type` is a qualified generic... so if `sub_type` isn't
    # qualified, it can't be a subtype.
    if is_base_generic(sub_type):
        return False

    # at this point we know that both types are qualified generics, so we just have to
    # compare their sub-types.
    sub_args = get_subtypes(sub_type)
    super_args = get_subtypes(super_type)
    return all(is_subtype(sub_arg, super_arg) for sub_arg, super_arg in zip(sub_args, super_args))


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
    if is_generic(typing_annotation):
        python_class = python_type(typing_annotation)

        for cls in vars(dtypes).values():
            if getattr(cls, 'python_type', None) is python_class:
                break
        else:
            raise NotImplementedError("Sorry, there doesn't seem to be a datatypes equivalent of {}".format(typing_annotation))

        if is_base_generic(typing_annotation):
            return cls

        subtypes = get_subtypes(typing_annotation)
        subtypes = tuple(typing_to_datatype(subtype) for subtype in subtypes)
        return cls[subtypes]

    return {
        typing.Any: dtypes.Any,
    }.get(typing_annotation, typing_annotation)
