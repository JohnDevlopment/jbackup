from __future__ import annotations

from ..actions import (load_action, _find_action_class, ActionNotLoaded,
                       ActionProperty, PropertyType)
from ..rules import Rule
from ..loader import load_module_from_file
from pathlib import Path
from dataclasses import dataclass
from typing import Any, Optional, cast

import pytest

@dataclass
class ActionParam:
    filename: str
    name: str

def test_run_action():
    d = Path(__file__).parent

    cls = load_action(d / '_testaction.py', 'testaction')

    # Instance the action
    rule = Rule(str(d / '_testrule.toml'))
    action = cls(rule)
    action.run()

class TestParams:
    PARAMTEST = [
        (0, PropertyType.INT),
        (0.01, PropertyType.FLOAT),
        (True, PropertyType.BOOL),
        ({}, PropertyType.DICT),
        ('', PropertyType.STRING),
        ([], PropertyType.LIST),
        (Path('.'), PropertyType.PATH),
    ]

    @pytest.mark.parametrize('value,expected', PARAMTEST)
    def test_params(self, value: Any, expected: PropertyType):
        prop = ActionProperty('someproperty', value)
        assert prop.property_type == expected, f"value is {prop.value!r}"
