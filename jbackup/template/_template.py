# Template for Actions

from __future__ import annotations
from typing import TYPE_CHECKING, cast
from jbackup.actions import ActionProperty, PropertyType
from jbackup.logging import get_logger, Level
from jbackup.utils import get_env
import sys

if TYPE_CHECKING:
    from jbackup.rules import Rule
    from typing import Any

class Action_Dummy:
    """An explanation for the action."""

    properties: list[ActionProperty] = []

    def __init__(self, rule: Rule):
        self.rule = rule
        self.propmapping = ActionProperty.get_properties('dummy', rule, self.properties)
        level = get_env('JBACKUP_LEVEL', Level.INFO, type_=int)
        self.logger = get_logger('dummy', cast(Level, level))

    def run(self) -> None:
        pass
