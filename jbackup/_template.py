# Template for Actions

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from jbackup.actions import Action, ActionProperty
    from jbackup.rules import Rule

class Action_Dummy:
    properties: list[ActionProperty] = []

    def __init__(self, rule: Rule) -> None:
        pass

    def run(self) -> None:
        pass
