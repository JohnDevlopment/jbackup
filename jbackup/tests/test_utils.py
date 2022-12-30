from pathlib import Path

from ..utils import XDictContainer, list_dirs
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
