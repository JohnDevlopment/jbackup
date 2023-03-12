from pathlib import Path

from ..utils import XDictContainer, get_env, EnvError, Stack
import pytest

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
    assert val is 3, "incorrect default value"

    with pytest.raises(EnvError):
        get_env('DOESNOTEXIST')

    with pytest.raises(TypeError):
        get_env('FAKEENV', type_=1) # pyright: ignore
