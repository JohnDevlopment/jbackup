from pathlib import Path

from ..utils import XDictContainer, list_dirs, get_env, EnvError
import pytest

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

def test_list_dirs() -> None:
    p = Path.cwd()
    dirs = list_dirs(str(p))
    assert dirs, "empty list"

    with pytest.raises(TypeError):
        list_dirs(p) # type: ignore

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
