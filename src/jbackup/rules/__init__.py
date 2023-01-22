# Rules

from __future__ import annotations
from pathlib import Path
from ..utils import list_dirs, Nil
from .config.toml_config_adapter import TOMLFile
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .config.config_protocol import ConfigFile

def list_rules(root: Path) -> list:
    return list_dirs(
        str(root / 'rules'))

class Rule:
    """A representation of a rule."""

    # TODO: add 'config' data descriptor

    def __init__(self, filename: str):
        if filename.endswith('.toml'):
            self.config: ConfigFile = TOMLFile(filename)

    def get(self, key: str, default: Any=None) -> Any:
        """
        Get the value associated with KEY in the config.

        Returns DEFAULT if KEY does not exist.
        """
        return self.config.get(key, default)

    def __getitem__(self, key: str) -> Any:
        nil = Nil()
        val = self.get(key, nil)
        if val is nil:
            raise KeyError(key)
        return val
