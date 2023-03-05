# Rules

from __future__ import annotations
from pathlib import Path
from ..utils import Nil
from .config.toml_config_adapter import TOMLFile
from .config import MissingOptionError, RuleParserError, MissingSectionError
from .config.config_protocol import ConfigFile
from typing import TYPE_CHECKING
import re

if TYPE_CHECKING:
    from typing import Any, Literal

__all__ = [
    # Classes
    'ConfigFile',
    'MissingOptionError',
    'MissingSectionError',
    'RuleParserError',
    'Rule',

    # Functions
    'parse_string'
]

class Rule:
    """A representation of a rule."""

    def __init__(self, filename: str, mode: Literal['r', 'w']='r'):
        """
        Open a rule file in the specified mode.

        The format of the rule file depends on the
        extension. MODE is either 'r' or 'w' for
        read and write operations, respectively.
        """
        kw: dict[str, Any] = {}
        if mode == 'w':
            kw['data'] = {
                'action': {'option': 'value'}
            }
        else:
            kw['func'] = parse_string

        if filename.endswith('.toml'):
            self._config = TOMLFile(filename, mode, **kw)

    @property
    def config(self) -> ConfigFile:
        """A config file."""
        return self._config

    def get(self, key: str, /, default: Any=None, safe: bool=False) -> Any:
        """
        Get the value associated with KEY in the config.

        if KEY does not exist, and SAFE is true, returns
        DEFAULT; otherwise MissingOptionError is raised.
        """
        try:
            return self.config.get(key, default)
        except MissingOptionError:
            if not safe: raise

        return default

    def __getitem__(self, key: str) -> Any:
        return self.get(key)

_re_type_tag = re.compile(r'@type\s+(\w+)\s+(.+)')

def parse_string(string: str) -> Any:
    """
    Parse a string and return potentially a different value.

    The string must conform to this syntax:
    `@type TYPE ...`, where TYPE is a type to
    return. If the syntax or the type are invalid,
    STRING is returned. If it is valid, then the
    rest of the string is converted to the selected
    type.

    The following types are accepted (case-insensitive):
      * path: converts the string into a Path
    """
    if (m := _re_type_tag.search(string)):
        _type, value = m.group(1, 2)
        if _type.lower() == 'path':
            return Path(value)

    return string
