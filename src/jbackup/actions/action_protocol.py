"""
Action protocol.

All future actions must conform to the structure
of this class.
"""

from __future__ import annotations
from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from ..rules import Rule
    from ..actions import ActionProperty

class Action(Protocol):
    """An interface to an action."""

    properties: list[ActionProperty]

    def __init__(self, rule: Rule):
        ...

    def run(self) -> None:
        ...
