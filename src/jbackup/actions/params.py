"""Subpackage for loading and running actions."""

from __future__ import annotations
from typing import TYPE_CHECKING, cast, overload
from enum import IntEnum, auto
from ..rules import Rule
import re

if TYPE_CHECKING:
    from re import Pattern
    from typing import Any

class PropertyType(IntEnum):
    """Property type."""

    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    STRING = auto()
    DICT = auto()
    LIST = auto()
    CUSTOM = auto()

class UndefinedProperty(Exception):
    """An error for undefined required properties."""

    def __init__(self, prop: str):
        self.__prop = prop

    def __str__(self) -> str:
        return f"missing value for required property '{self.__prop}'"

class ActionPropertyMapping(dict):
    """A mapping of properties."""

    def __init__(self, mapping: dict[str, ActionProperty]):
        newdict = {k: v.value for k, v in mapping.items()}
        super().__init__(newdict)

    def __repr__(self) -> str:
        dictstr = super().__repr__()
        return f"ActionPropertyMapping({dictstr})"

    def __getitem__(self, key: str, /) -> Any:
        return super().__getitem__(key)

    def get(self, key: str, default: Any=None, /) -> Any:
        return super().get(key, default)

class ActionProperty:
    """
    An action parameter.

    self.name can contain letters and underscores,
    as well as periods or forward slashes.

    self.value contains the property value. Its type
    is used to set self.property_type.
    """

    __slots__ = ('__name', '__value', '__property_type', '__type_name',
                 '__doc', 'optional')

    _clsname_pattern: Pattern = re.compile(r"<class '(.+)'>")

    @classmethod
    def _get_type_name(cls, atype: type):
        """Return the string name of ATYPE."""
        if not isinstance(atype, type):
            raise TypeError(f"{atype} is not derived from type")

        pt = {
            int: PropertyType.INT,
            float: PropertyType.FLOAT,
            bool: PropertyType.BOOL,
            str: PropertyType.STRING,
            dict: PropertyType.DICT,
            list: PropertyType.LIST
        }.get(atype, PropertyType.CUSTOM)

        m = cls._clsname_pattern.search(str(cls))
        assert m

        return pt, m[1]

    def __init__(self, name: str, value: Any, /,
                 optional: bool=False, doc: str | None=None) -> None:
        """
        Construct an ActionProperty object with a NAME and VALUE.

        If OPTIONAL is True, this property does not have to be set
        by a rule.
        """
        if not name:
            raise ValueError("empty name")

        self.__name: str = name
        self.__value: Any = value
        pt, tn = self._get_type_name(type(self.__value))
        self.__property_type: PropertyType = pt
        self.__type_name: str = tn
        self.__doc = doc
        self.optional = optional

    @staticmethod
    def get_properties(action: str, rule: Rule, *properties) -> ActionPropertyMapping:
        """
        Returns a list of properties with their values filled in.

        See ActionProperty for more info.
        """
        lproperties: list[ActionProperty] = list(properties)
        for prop in lproperties:
            propname: str = prop.name.replace('.', '/')
            default = prop.value
            prop.value = rule.get(f"{action}/{propname}", default, prop.optional)

        return ActionPropertyMapping({prop.name: prop for prop in lproperties})

    @property
    def name(self) -> str:
        """The name of the property."""
        return self.__name

    @property
    def property_type(self) -> PropertyType:
        """The property type."""
        return self.__property_type

    @property
    def property_type_name(self):
        """A string giving"""
        return self.__type_name

    @property
    def value(self) -> Any:
        """The property's value; also sets self.property_type."""
        return self.__value

    @property
    def doc(self) -> str:
        """Documentation string."""
        return self.__doc or ""

    def __str__(self) -> str:
        string = f"{self.property_type.name} {self.name}"
        doc = self.doc
        if doc:
            string += f" -- {doc}"
        return string

    @value.setter
    def value(self, value: Any) -> None:
        if value is None and not self.optional:
            raise UndefinedProperty(self.__name)
        self.__value = value
        pt, tn = self._get_type_name(type(self.__value))
        self.__property_type: PropertyType = pt
        self.__type_name: str = tn
