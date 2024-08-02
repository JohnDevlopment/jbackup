"""
Types: protocols, aliases, and generics
"""

from __future__ import annotations
from typing import Protocol, TypeAlias, TypeVar

T = TypeVar('T')
Tc = TypeVar('Tc', covariant=True)

class Pathlike(Protocol[Tc]):
    """
    A protocol of Path-like classes.
    """

    def __fspath__(self) -> Tc:
        ...

    def exists(self) -> bool:
        """
        Whether the path exists.
        """
        ...

    def is_absolute(self) -> bool:
        """
        Whether the path is an absolute one.
        """
        ...

    def __str__(self) -> str:
        ...

StrPath: TypeAlias = str | Pathlike[str]

if __name__ == '__main__':
    raise NotImplementedError
