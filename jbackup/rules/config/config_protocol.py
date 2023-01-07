"""Defines an interface to rule config files."""

from typing import Protocol, Any, Optional
from ...utils import BufferedReadFileDescriptor

class ConfigFile(Protocol):
    """Interface to a config file."""

    @staticmethod
    def parse_file(fileobj_or_string: str | BufferedReadFileDescriptor) -> dict[str, Any]:
        """
        Parse FILENAME and return a dictionary.

        The returned dictionary has the same general
        structure as FILENAME.

        This should be called by the class initializer.
        """
        ...

    def get(self, key: str, default=None) -> Any: # type: ignore
        """
        Return the value associated with KEY.

        If KEY does not exist, DEFAULT is returned.
        """
        ...
