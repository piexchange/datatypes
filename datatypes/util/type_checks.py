
import typing

__all__ = ['instancecheck']


def _typecheck_iterable(iterable, type_args):
    if len(type_args) != 1:
        raise TypeError("Generic iterables must have exactly 1 type argument; found {}".format(type_args))

    type_ = type_args[0]
    return all(instancecheck(val, type_) for val in iterable)


def _typecheck_mapping(mapping, type_args):
    return _typecheck_itemsview(mapping.items(), type_args)


def _typecheck_itemsview(itemsview, type_args):
    if len(type_args) != 2:
        raise TypeError("Generic mappings must have exactly 2 type arguments; found {}".format(type_args))

    key_type, value_type = type_args
    return all(instancecheck(key, key_type) and instancecheck(val, value_type) for key, val in itemsview)


def _typecheck_tuple(tup, type_args):
    if len(tup) != len(type_args):
        return False

    return all(instancecheck(val, type_) for val, type_ in zip(tup, type_args))


_ORIGIN_TYPE_CHECKERS = {
    # iterables
    typing.Container: _typecheck_iterable,
    typing.Collection: _typecheck_iterable,
    typing.AbstractSet: _typecheck_iterable,
    typing.MutableSet: _typecheck_iterable,
    typing.Sequence: _typecheck_iterable,
    typing.MutableSequence: _typecheck_iterable,
    typing.ByteString: _typecheck_iterable,
    typing.Deque: _typecheck_iterable,
    typing.List: _typecheck_iterable,
    typing.Set: _typecheck_iterable,
    typing.FrozenSet: _typecheck_iterable,
    typing.KeysView: _typecheck_iterable,
    typing.ValuesView: _typecheck_iterable,
    typing.AsyncIterable: _typecheck_iterable,

    # mappings
    typing.Mapping: _typecheck_mapping,
    typing.MutableMapping: _typecheck_mapping,
    typing.MappingView: _typecheck_mapping,
    typing.ItemsView: _typecheck_itemsview,
    typing.Dict: _typecheck_mapping,
    typing.DefaultDict: _typecheck_mapping,
    typing.Counter: _typecheck_mapping,
    typing.ChainMap: _typecheck_mapping,

    # other
    typing.Tuple: _typecheck_tuple,
}


# typing module compatibility functions
def _is_base_generic(cls):
    return bool(getattr(cls, '__parameters__', False))


def _is_generic_with_arguments(cls):
    return bool(getattr(cls, '__args__', False))


def _get_base_generic(cls):
    # python 3.7
    if hasattr(cls, '_name'):
        base_name = cls._name
        return getattr(typing, base_name)
    # python 3.6 and older
    else:
        return cls._gorg


def _get_python_type(cls):
    # python 3.6 and older
    if hasattr(cls, '__extra__'):
        return cls.__extra__
    # python 3.7
    else:
        return cls.__origin__
# end of typing compatibility


def instancecheck(obj, type_):
    if _is_base_generic(type_):
        python_type = _get_python_type(type_)
        return isinstance(obj, python_type)

    if _is_generic_with_arguments(type_):
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
