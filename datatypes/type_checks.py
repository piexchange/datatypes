
import inspect
import typing

from datatypes.types.generics import GenericMeta, QualifiedGenericMeta
from datatypes.introspection import *
from datatypes.introspection import _is_protocol, _get_name, _get_python_type


__all__ = ['is_instance', 'is_subtype']


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

        # if any of the existing annotations don't match the type, we'll return False.
        # Then, if any annotations are missing, we'll throw an exception.
        for param, expected_type in zip(sig.parameters.values(), param_types):
            param_type = param.annotation
            if param_type is inspect.Parameter.empty:
                missing_annotations.append(param)
                continue

            # FIXME: add support for TypeVars
            if isinstance(expected_type, typing.TypeVar) or isinstance(param_type, typing.TypeVar):
                raise NotImplementedError('TypeVars are not supported')

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


def _instancecheck_protocol(value, proto):
    def is_abstract(thing):
        return getattr(thing, '__isabstractmethod__', False)

    def extract_inner_methods(thing):
        if isinstance(thing, property):
            return {
                'property.fget': thing.fget,
                'property.fset': thing.fset,
                'property.fdel': thing.fdel
            }

        if isinstance(thing, classmethod):
            return {'classmethod.__func__': thing.__func__}

        if isinstance(thing, staticmethod):
            return {'staticmethod.__func__': thing.__func__}

        return {'': thing}

    abcs = {}
    seen = set()
    for cls in proto.mro():
        for name, val in vars(cls).items():
            if name in seen:
                continue
            seen.add(name)

            abstracts = {k for k, meth in extract_inner_methods(val).items() if is_abstract(meth)}
            if abstracts:
                abcs[name] = abstracts

    for name, abstracts in abcs.items():
        try:
            meth = getattr(value, name)
        except AttributeError:
            return False

        abcs = {k for k, m in extract_inner_methods(meth).items() if is_abstract(m)}
        if abstracts & abcs:
            return False

    return True


_SPECIAL_INSTANCE_CHECKERS = {
    'Union': _instancecheck_union,
    'Callable': _instancecheck_callable,
    'Type': _instancecheck_type,
    'Any': lambda v, t: True,
}


def is_instance(obj, type_):
    if type_.__module__ == 'typing':
        if _is_protocol(type_):
            return _instancecheck_protocol(obj, type_)

        if is_qualified_generic(type_):
            base_generic = get_base_generic(type_)
        else:
            base_generic = type_
        name = _get_name(base_generic)

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

        type_args = get_subtypes(type_)
        return validator(obj, type_args)

    return isinstance(obj, type_)


def is_subtype(sub_type, super_type):
    if not is_generic(sub_type):
        python_super = get_python_type(super_type)
        return issubclass(sub_type, python_super)

    # at this point we know `sub_type` is a generic
    python_sub = get_python_type(sub_type)
    python_super = get_python_type(super_type)
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
