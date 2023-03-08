# Test action

from __future__ import annotations
from typing import TYPE_CHECKING
from jbackup.actions import ActionProperty

if TYPE_CHECKING:
    from jbackup.rules import Rule
    from typing import Optional, Any, cast

class Action_Test:
    properties: list[ActionProperty] = [
        ActionProperty('message', ''),
        ActionProperty('extra-message', None, optional=True)
    ]

    def __init__(self, rule: Rule) -> None:
        self.rule = rule
        self.propmapping = ActionProperty.get_properties('test', rule, self.properties)

    def run(self) -> None:
        print("== Run action 'test' ==")
        print(self.propmapping['message'])
        exmsg: str = self.propmapping.get('extra-message', '')
        if exmsg:
            print(exmsg)
        print("== End of action ==")
