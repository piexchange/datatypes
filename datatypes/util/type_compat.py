
import typing

from datatypes import types as dtypes
from datatypes.introspection import is_generic, is_base_generic, get_python_type, get_subtypes


__all__ = ['typing_to_datatype']



def typing_to_datatype(typing_annotation):
    """
    Given a class or object from the typing module as input, returns the corresponding datatypes class. If the input
    is any other class, it is returned unchanged.
    """
    if is_generic(typing_annotation):
        python_class = get_python_type(typing_annotation)

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
