
from datatypes import types as dtypes
from datatypes.introspection import is_generic, is_base_generic, get_base_generic, get_python_type, get_subtypes


__all__ = ['class_to_datatype']


_CLASS_TO_DTYPE = {dtype.python_type: dtype for dtype in vars(dtypes).values() if hasattr(dtype, 'python_type')}
_TYPING_TO_DTYPE = {dtype.typing_type: dtype for dtype in vars(dtypes).values() if hasattr(dtype, 'typing_type')}


def class_to_datatype(cls):
    """
    Given a class or type annotation as input, returns the corresponding datatypes class. If no equivalent
    datatype exists, the input is returned unchanged.
    """
    if cls.__module__ not in {'typing', 'datatypes'}:
        return _CLASS_TO_DTYPE.get(cls, cls)

    if not is_generic(cls) or is_base_generic(cls):
        if cls.__module__ == 'typing':
            return _TYPING_TO_DTYPE.get(cls, cls)

        return _CLASS_TO_DTYPE.get(cls, cls)

    # at this point we know the class is a qualified generic
    base = get_base_generic(cls)
    base = class_to_datatype(base)

    subtypes = get_subtypes(cls)
    subtypes = tuple(class_to_datatype(subtype) for subtype in subtypes)
    if len(subtypes) == 1:
        return base[subtypes[0]]
    return base[subtypes]


