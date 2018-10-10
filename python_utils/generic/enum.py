"""Enum generic utils class"""
from enum import Enum


class EnumWithDesc(Enum):
    """Enum class that accepts a second description arg"""

    def __new__(cls, key, desc):
        obj = object.__new__(cls)
        obj._value_ = key  # pylint: disable W0212
        obj.desc = desc
        return obj
