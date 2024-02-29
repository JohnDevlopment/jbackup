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

class TestProperties:
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
    def test_props(self, value: Any, expected: PropertyType):
        prop = ActionProperty('someproperty', value, doc=f"some property that is a {expected.name}")
        assert prop.property_type == expected, f"value is {prop.value!r}"
        print(prop)

    def test_exception_strings(self, capsys: pytest.CaptureFixture):
        from ..actions import PropertyTypeError, UndefinedProperty
        import re

        # Non-index exception string fits expected format?
        e = PropertyTypeError('property', PropertyType.INT,
                              [PropertyType.STRING, PropertyType.BOOL])

        print(e)
        captured = capsys.readouterr()

        pattern = r"invalid action-parameter '([a-zA-Z.]+)' \(type is (.+)\)"
        m = re.match(pattern, captured.out)
        assert m, f"'{captured.out}' did not match pattern"
        name, _type = m.group(1, 2)
        assert name == "property"
        assert _type == "INT"

        # Index exception string
        e = PropertyTypeError('list-property', PropertyType.STRING,
                              [PropertyType.INT, PropertyType.FLOAT], index=1)
        print(e)
        captured = capsys.readouterr()

        pattern = r"invalid index ([0-9]) of action-parameter '(.+)' " \
            + r"\(type is (.+)\)"
        m = re.match(pattern, captured.out)
        assert m, f"'{captured.out}' did not match pattern"
        index, name, _type = m.group(1, 2, 3)
        assert index == "1"
        assert name == "list-property"
        assert _type == "STRING"

    def test_errors(self, capsys: pytest.CaptureFixture):
        from ..actions import PropertyTypeError, UndefinedProperty

        with pytest.raises(ValueError):
            ActionProperty('', '')

    def test_properties(self):
        prop = ActionProperty('foo', 'bar', doc="doc")
        prop.property_type_name
        assert prop.doc
        with pytest.raises(UndefinedProperty):
            prop.value = None
