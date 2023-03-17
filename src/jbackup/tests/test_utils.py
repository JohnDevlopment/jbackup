from __future__ import annotations
from pathlib import Path
from ..utils import XDictContainer, get_env, EnvError, Stack
from .._path import get_data_path
from typing import TYPE_CHECKING, cast
import pytest, itertools

if TYPE_CHECKING:
    from typing import Callable, Literal

# Helpers

def _random_filename(n: int, suffix: str="") -> str:
    import random
    randstr: str = ""
    for i in range(n):
        randstr += chr(random.randint(65, 122))
    return randstr + suffix

# Classes

class TestListAvailable:
    def _get(self, func: Callable[[Literal['system', 'user']], list[str]]) -> set[str]:
        return set(itertools.chain(func('system'), func('user')))

    def test_actions(self):
        from ..utils import list_available_actions
        _dir = get_data_path() / "actions"
        _file = _dir / _random_filename(4, ".py")

        print(f"{__class__}::test_actions: open {_file}")
        with open(_file, 'w') as fd:
            fd.write("# Some module")
        actions = self._get(list_available_actions)
        _file.unlink()
        assert actions

    def test_rules(self):
        from ..utils import list_available_rules
        _dir = get_data_path() / "rules"
        _file = _dir / _random_filename(4, ".toml")

        print(f"{__class__}::test_rules: open {_file}")
        with open(_file, 'w') as fd:
            fd.write("key=value")
        rules = self._get(list_available_rules)
        _file.unlink()
        assert rules

# Individual tests

def test_stack() -> None:
    stack1 = Stack([1, 2, 3])
    assert len(stack1) == 3
    assert 1 in stack1
    assert 2 in stack1
    assert 3 in stack1

    stack2: Stack[int] = Stack([1, 2, 3])
    assert stack1 == stack2

    assert stack2.pop() == 1
    assert stack2.pop() == 2
    assert stack2.pop() == 3

    stack1: Stack[int] = Stack([1, 2, 3, 4, 5])
    for i in range(1, 6):
        stack2.push(i)
    assert stack1 == stack2

    stack1.pop()
    assert stack1 == Stack([2, 3, 4, 5])
    assert stack1 != stack2
    assert stack1 > stack2
    assert stack1 >= stack2
    assert stack2 < stack1
    assert stack2 <= stack1

    assert repr(stack1) == "Stack([2, 3, 4, 5])"
    assert repr(stack2) == "Stack([1, 2, 3, 4, 5])"

def test_xdict_container() -> None:
    ctn = XDictContainer({
        'employees': {
            'John': 1,
            'Bob': 2,
            'Alinda': 3,
            'sub': {}
        },
        'count': 3
    })

    assert ctn['employees/John'] == 1
    assert ctn['employees/Bob'] == 2
    assert ctn['employees/Alinda'] == 3
    assert ctn['count'] == 3

    assert not ctn['employees/sub']

    with pytest.raises(KeyError):
        ctn['does/notexist']

    with pytest.raises(KeyError):
        ctn['employees/Joe']

@pytest.mark.parametrize('env,extype',
                         [('JBACKUP_BOOL', bool),
                          ('JBACKUP_STRING', str),
                          ('JBACKUP_INT', int),
                          ('JBACKUP_FLOAT', float),
                          ('JBACKUP_LIST', list)])
def test_get_env_casted(env: str, extype: type) -> None:
    val = get_env(env, type_=extype)
    assert isinstance(val, extype), \
        f"{env} returned {type(val)}, not {extype} as expected"

    if extype == list:
        assert len(val) == 3

def test_get_env_errors() -> None:
    val = get_env('DOESNOTEXIST', 3)
    # TODO: change 'is' to '=='
    assert val is 3, "incorrect default value"

    with pytest.raises(EnvError):
        get_env('DOESNOTEXIST')

    with pytest.raises(TypeError):
        get_env('FAKEENV', type_=1) # pyright: ignore
