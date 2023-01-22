"""Subpackage for loading and running actions."""

from __future__ import annotations
from typing import Optional, Any, TYPE_CHECKING
from dataclasses import dataclass
from enum import IntEnum, auto
from ..utils import Nil
import re

if TYPE_CHECKING:
    from re import Pattern
    from typing import ClassVar, Union

class PropertyType(IntEnum):
    """Property type."""

    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    STRING = auto()
    DICT = auto()
    LIST = auto()

class UndefinedProperty(Exception):
    """An error for undefined required properties."""

    def __init__(self, prop: str):
        self.__prop = prop

    def __str__(self) -> str:
        return f"missing value for required property '{self.__prop}'"

class ActionProperty:
    """
    An action parameter.

    self.name can contain letters and underscores,
    as well as periods or forward slashes.

    self.value contains the property value. Its type
    is used to set self.property_type.
    """

    #_clsname_pattern: Pattern = re.compile(r"<class '(.+)'>")

    @classmethod
    def _get_type_name(cls, atype: type) -> PropertyType:
        """Return the string name of ATYPE."""
        if not isinstance(atype, type):
            raise TypeError(f"{atype} is not derived from type")

        #if (m := cls._clsname_pattern.search(str(cls))):
        #    return m[1]

        return {
            int: PropertyType.INT,
            float: PropertyType.FLOAT,
            bool: PropertyType.BOOL,
            str: PropertyType.STRING,
            dict: PropertyType.DICT,
            list: PropertyType.LIST
        }[atype]

    def __init__(self, name: str, value: Any, /, optional: bool=False) -> None:
        """
        Construct an ActionProperty object with a NAME and VALUE.

        If OPTIONAL is True, this property does not have to be set
        by a rule.
        """
        self.__name: str = name
        self.__value: Any = value
        self.__property_type: PropertyType = self._get_type_name(type(self.__value))
        self.optional = optional

    @property
    def name(self) -> str:
        """The name of the property."""
        return self.__name

    @property
    def property_type(self) -> PropertyType:
        """The property type."""
        return self.__property_type

    @property
    def value(self) -> Any:
        """The property's value; also sets self.property_type."""
        return self.__value

    @value.setter
    def value(self, value: Any) -> None:
        if value is None and not self.optional:
            raise UndefinedProperty(self.__name)
        self.__value = value
        self.__property_type = self._get_type_name(type(self.__value))
