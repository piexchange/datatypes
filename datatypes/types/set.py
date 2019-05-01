
import typing

from .collection import Collection

__all__ = ['Set']


class Set(Collection):
    python_type = set
    typing_type = typing.Set