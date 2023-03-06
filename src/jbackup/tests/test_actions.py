from __future__ import annotations

from jbackup.actions.params import UndefinedProperty

from ..actions import load_action, ActionNotLoaded, ActionProperty, PropertyType
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

    def test_property_mapping(self):
        from ..actions import ActionPropertyMapping
        d = ActionPropertyMapping({
            'property1': ActionProperty('property1', 1),
            'property2': ActionProperty('property2', 2),
            'property3.subproperty': ActionProperty('property3.subproperty', 3.1),
        })
        print(f"{d!r}")

    @pytest.mark.parametrize('value,expected', PARAMTEST)
    def test_params(self, value: Any, expected: PropertyType):
        prop = ActionProperty('someproperty', value, doc=f"some property that is a {expected.name}")
        assert prop.property_type == expected, f"value is {prop.value!r}"
        print(prop)

    def test_errors(self, capsys):
        from ..actions import PropertyTypeError, UndefinedProperty

        e = PropertyTypeError('property', PropertyType.INT.name,
                              [PropertyType.STRING, PropertyType.BOOL])
        print(e)

        e = PropertyTypeError('properties', PropertyType.INT.name,
                              [PropertyType.STRING, PropertyType.BOOL], index=0)
        print(e)

        e = UndefinedProperty('property')
        print(e)

        with pytest.raises(ValueError):
            ActionProperty('', '')

    def test_properties(self):
        prop = ActionProperty('foo', 'bar', doc="doc")
        prop.property_type_name
        assert prop.doc
        with pytest.raises(UndefinedProperty):
            prop.value = None
