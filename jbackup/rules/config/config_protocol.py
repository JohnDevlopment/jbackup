"""Defines an interface to rule config files."""

from __future__ import annotations
from typing import Protocol, Any, BinaryIO

class ConfigFile(Protocol):
    """Interface to a config file."""

    @staticmethod
    def write_file(fp: BinaryIO, obj):
        """Write an object to file."""
        ...

    @staticmethod
    def parse_file(fp: BinaryIO) -> dict[str, Any]:
        """
        Parse FILENAME and return a dictionary.

        The returned dictionary has the same general
        structure as the input.

        This should be called by the class initializer.
        """
        ...

    def get(self, key: str, default=None) -> Any: # type: ignore
        """
        Return the value associated with KEY.

        If KEY does not exist, DEFAULT is returned.
        """
        ...
