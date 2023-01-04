"""Subpackage for loading and running actions."""

from __future__ import annotations
from typing import Optional, Any, ClassVar, TYPE_CHECKING
from dataclasses import dataclass
import re

from enum import IntFlag, auto

#_MappingType = dict[str, Any]

if TYPE_CHECKING:
    from re import Pattern

class PropertyType(IntFlag):
    """Property type."""

    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    STRING = auto()
    DICT = auto()
    LIST = auto()
    OPTIONAL = auto()

@dataclass(slots=True)
class ActionProperty:
    """An action parameter."""

    _clsname_pattern: ClassVar[Pattern] = re.compile(r"<class '(.+)'>")

    name: str
    value: Any
    param_type: Optional[str] = None

    @classmethod
    def _get_type_name(cls, atype: type) -> Optional[str]:
        """Return the string name of ATYPE."""
        if not isinstance(atype, type):
            raise TypeError(f"{atype} is not derived from type")

        if (m := cls._clsname_pattern.search(str(cls))):
            return m[1]

    def __post_init__(self) -> None:
        if self.param_type is None:
            self.param_type = self._get_type_name(type(self.value))
