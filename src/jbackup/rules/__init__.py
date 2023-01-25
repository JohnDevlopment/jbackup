# Rules

from __future__ import annotations
from pathlib import Path
from ..utils import list_dirs, Nil
from .config.toml_config_adapter import TOMLFile
from .config import MissingOptionError
from .config.config_protocol import ConfigFile
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Literal

def list_rules(root: Path) -> list:
    return list_dirs(str(root / 'rules'))

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
        nil = Nil()
        val = self.get(key, nil)
        if val is nil:
            raise KeyError(key)
        return val
