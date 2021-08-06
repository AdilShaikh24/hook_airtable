import collections
from typing import Mapping, Any


# Created AttrDict, so can we access dict keys with attribute like.
class AttrDict:
    def __init__(self, data: Mapping[Any, Any]):
        self.__data = data

    def __getattr__(self, item):
        value = self.__data[item]
        if isinstance(value, collections.Mapping):
            return AttrDict(value)
        return value
