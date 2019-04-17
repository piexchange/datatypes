
import typing

from .collection import Collection

__all__ = ['List']


class List(Collection):
    python_type = list
    typing_type = typing.List
