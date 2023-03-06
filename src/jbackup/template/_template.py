# Template for Actions

from __future__ import annotations
from typing import TYPE_CHECKING
from jbackup.actions import ActionProperty
from jbackup.logging import get_logger
from jbackup.utils import get_env
import logging, sys

if TYPE_CHECKING:
    from jbackup.rules import Rule
    from typing import Optional, Any, cast

class Action_Dummy:
    """An explanation for the action."""

    properties: list[ActionProperty] = []

    def __init__(self, rule: Rule):
        self.rule = rule
        self.propmapping = ActionProperty.get_properties('dummy', rule, *self.properties)
        self.logger = get_logger('dummy')
        level = get_env('JBACKUP_LEVEL', logging.INFO, type_=int)
        self.logger.setLevel(level)

    def run(self) -> None:
        pass
