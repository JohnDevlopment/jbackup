from ..actions import load_action, _find_action_class, ActionNotLoaded
from ..rules import Rule
from ..loader import load_module_from_file
from pathlib import Path
from dataclasses import dataclass
import pytest

@dataclass
class ActionParam:
    filename: str
    name: str

@pytest.fixture
def testaction() -> ActionParam:
    return ActionParam(
        str(Path(__file__).parent / '_testaction.py'),
        'testaction'
    )

def test_action_works(testaction: ActionParam):
    mod = load_module_from_file(testaction.filename,
                                testaction.name)
    cls = _find_action_class(mod)
    assert cls is not None

@pytest.mark.parametrize('mod,modname',
                         [('_testaction.py', 'testaction'),
                          ('_testbadaction.py', 'badaction')])
def test_create_action(mod: str, modname: str):
    assert mod.endswith('.py'), "not .py file"

    filename = str(Path(__file__).parent / mod)

    if modname == 'badaction':
        with pytest.raises(ActionNotLoaded):
            cls = load_action(filename, modname)
        return

    cls = load_action(filename, modname)

    rule = Rule(str(
        Path(__file__).parent / '_testrule.toml'))

    action = cls(rule)
    action.run()
