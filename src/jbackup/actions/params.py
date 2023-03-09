"""Subpackage for loading and running actions."""

from __future__ import annotations
from typing import TYPE_CHECKING
from enum import IntEnum, auto
from ..rules import Rule
from pathlib import Path
import re

if TYPE_CHECKING:
    from re import Pattern
    from typing import Any, Iterable

class PropertyType(IntEnum):
    """Property type."""

    NONE = auto()
    BOOL = auto()
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    LIST = auto()
    DICT = auto()
    PATH = auto()
    CUSTOM = auto()

class PropertyTypeError(TypeError):
    """An error for an action parameter with the wrong type."""

    def __init__(self, key: str, key_type: str | type, types: Iterable[PropertyType],
                 *args, index: int=-1, **kw):
        """
        Construct the error with a KEY and its associated TYPE.

        KEY_TYPE describes the parameter type.
        TYPES is a list of allowed `PropertType`s. The INDEX
        keyword argument, if present, indicates a list, with
        it specifying which element is invalid.
        """
        super().__init__(*args, **kw)
        self.key = key
        self.key_type = key_type
        self.types = list(types)
        self.index = index

    def __str__(self) -> str:
        if self.index < 0:
            msg = f"invalid action-parameter '{self.key}' (type is {self.key_type})"
        else:
            msg = f"invalid index {self.index} of action-parameter " \
                + f"'{self.key}' (type is {self.key_type})"

        if self.types:
            validtypes = ". valid types are: " + ", ".join(map(lambda t: t.name, self.types))
            msg += validtypes
        return msg

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
    """A property for an action."""

    _clsname_pattern: Pattern[str] = re.compile(r"<class '(.+)'>")

    _property_type_map: dict[type, PropertyType] = {
        int: PropertyType.INT,
        float: PropertyType.FLOAT,
        bool: PropertyType.BOOL,
        str: PropertyType.STRING,
        dict: PropertyType.DICT,
        list: PropertyType.LIST,
        type(None): PropertyType.NONE
    }

    @classmethod
    def _get_type_name(cls, atype: type) -> tuple[PropertyType, str]:
        """Return the string name of ATYPE."""
        if not isinstance(atype, type):
            raise TypeError(f"{atype} is not derived from `type'")

        typename = atype.__name__
        pt = cls._property_type_map.get(atype, PropertyType.CUSTOM)
        if pt == PropertyType.CUSTOM:
            if issubclass(atype, Path):
                pt = PropertyType.PATH
            elif typename == 'NoneType':
                pt = PropertyType.NONE

        return pt, typename

    def __init__(self, name: str, value: Any, /,
                 optional: bool=False, doc: str | None=None) -> None:
        """
        Construct an ActionProperty object with a NAME and VALUE.

        Unless OPTIONAL is true, UndefinedProperty is raised
        if the property is not set by the rule. DOC is a
        documentation string about the action property.
        """
        if not name:
            raise ValueError("empty name")

        self._name = name
        self._value = value
        pt, tn = self._get_type_name(type(self._value))
        self._property_type = pt
        self._type_name = tn
        self._doc = doc
        self._optional = optional
        self._types = types or []

    @staticmethod
    def get_properties(action: str, rule: Rule, properties: list[ActionProperty]) -> ActionPropertyMapping:
        """
        Returns a dictionary of PROPERTIES with their value set by a RULE.

        Each property's value is set by RULE using a string
        '{ACTION}/x', where x is the name of the of the
        property.

        Property names are translated to a format supported by the
        rule.

        The return value is a mapping of property names and their values.
        """
        lproperties = properties.copy()
        for prop in lproperties:
            propname = prop.name.replace('.', '/')
            default = prop.value
            value = rule.get(f"{action}/{propname}", default, prop._optional)
            prop.value = value

        return ActionPropertyMapping({prop.name: prop for prop in lproperties})

    @property
    def name(self) -> str:
        """The name of the property."""
        return self._name

    @property
    def property_type(self) -> PropertyType:
        """The property type."""
        return self._property_type

    @property
    def property_type_name(self) -> str:
        """The string name of the type."""
        return self._type_name

    @property
    def value(self) -> Any:
        """The property's value; also sets self.property_type."""
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        if value is None and not self._optional:
            raise UndefinedProperty(self._name)
        self._value = value
        pt, tn = self._get_type_name(type(self._value))
        self._property_type = pt
        self._type_name = tn

    @property
    def doc(self) -> str:
        """Documentation string."""
        return self._doc or ""

    def __str__(self) -> str:
        string = f"{self.property_type.name} {self.name}"
        doc = self.doc
        if doc:
            string += f" -- {doc}"
        return string
