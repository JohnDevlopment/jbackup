# Template for Actions

from __future__ import annotations
from typing import TYPE_CHECKING
from jbackup.actions import ActionProperty

if TYPE_CHECKING:
    from jbackup.rules import Rule

class Action_Dummy:
    properties: list[ActionProperty] = []

    def __init__(self, rule: Rule):
        self.__properties = self.properties.copy()

        for prop in self.__properties:
            propname: str = prop.name.replace('.', '/')
            prop.value = rule.get(propname)

    def run(self) -> None:
        pass
