from __future__ import annotations

from jbackup.actions.params import UndefinedProperty

from ..actions import (load_action, _find_action_class, ActionNotLoaded,
                       ActionProperty, PropertyType, _DocstringFormatter)
from ..rules import Rule
from pathlib import Path
from dataclasses import dataclass
from typing import Any
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

def test_errors():
    f = Path(__file__).parent / '_testbadaction.py'
    with pytest.raises(ActionNotLoaded):
        load_action(f, 'badaction')

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

    def test_errors(self):
        with pytest.raises(ValueError):
            ActionProperty('', '')

    def test_properties(self):
        prop = ActionProperty('foo', 'bar', doc="doc")
        prop.property_type_name
        assert prop.doc
        with pytest.raises(UndefinedProperty):
            prop.value = None
