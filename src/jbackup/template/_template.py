# Template for Actions

from __future__ import annotations
from typing import TYPE_CHECKING
from jbackup.actions import ActionProperty

if TYPE_CHECKING:
    from jbackup.rules import Rule
    from typing import Optional, Any, cast

class Action_Dummy:
    """An explanation for the action."""

    properties: list[ActionProperty] = []

    def __init__(self, rule: Rule):
        self.rule = rule
        self.propmapping = ActionProperty.get_properties('dummy', rule, *self.properties)

    def run(self) -> None:
        pass
