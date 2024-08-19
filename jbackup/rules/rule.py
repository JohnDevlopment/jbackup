"""
Definition of Rule class.
"""

from __future__ import annotations
from pathlib import Path
from typing import TYPE_CHECKING

from .. import APPNAME
from ..exceptions import OSErrorFactory
from .config.toml_config_adapter import TOMLFile
from .config.config_protocol import ConfigFile
from .exceptions import MissingOptionError, RuleParserError

if TYPE_CHECKING:
    from typing import Any
    from ..types import StrPath

from platformdirs import user_data_path

class Rule:
    """
    A representation of a rule.
    """

    def __init__(self, filename: StrPath, mode='r', data=None):
        """
        Open a rule file in the specified mode.

        If MODE is r, then the rule is initialized from the file
        pointed to at FILENAME. But if the MODE is w, then DATA is
        written to the file.

        DATA is a dictionary mapping sections to keys, for example:

        {"compression": {"verbose": True, archive=""}}
        """
        filename = Path(filename)

        if not(mode in ("w", "r")):
            raise RuleParserError(f"Invalid mode '{mode}', must be r or w")

        if filename.suffix != ".toml":
            raise RuleParserError(f"Invalid filename '{filename}', must be a TOML file")

        self._config = TOMLFile(str(filename), mode, data=data)

    @staticmethod
    def get_path():
        """The directory where the rules are located."""
        return user_data_path(APPNAME) / "rules"

    @staticmethod
    def list_rules():
        d = user_data_path(APPNAME) / "rules"
        filt = filter(lambda x: x.suffix == ".toml", d.iterdir())
        return list(filt)

    @classmethod
    def find(cls, name: str, read=False):
        """
        Fetch a rule from the standard rule path.

        NAME is the name of a rule file without the leading path and
        its extension (e.g., "somerule" => somerule.toml).

        If MODE is either 'r' or 'w', a Rule is returned, if it
        exists; otherwise, the absolute path is returned, if it
        exists.

        If NAME does not exist, then FileNotFoundError is raised.
        """
        fp = user_data_path(APPNAME) / "rules" / f"{name}.toml"

        if fp.exists():
            return cls(str(fp), mode='r') if read else fp

        raise OSErrorFactory.FileNotFoundError(fp)

    @property
    def config(self) -> ConfigFile:
        """A config file."""
        return self._config

    def get(self, key: str, /, default=None, safe=False):
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

    def __getitem__(self, key: str):
        """
        Get the value associated with a key.

        Basically the same as self.get(), except MissingOptionError
        is raised if said key does not exist.
        """
        return self.get(key)
