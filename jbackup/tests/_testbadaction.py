# Test action that has no action class

from __future__ import annotations
from typing import TYPE_CHECKING
from jbackup.actions import ActionProperty

if TYPE_CHECKING:
    from jbackup.rules import Rule

class Test:
    properties: list[ActionProperty] = [
        ActionProperty('message', 'This is a test action')
    ]

    def __init__(self, rule: Rule) -> None:
        self.rule = rule

    def run(self) -> None:
        print("Dummy test")
