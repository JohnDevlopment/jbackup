from ..rules.utils import read_toml_file, read_toml_string
from tempfile import NamedTemporaryFile
from typing import Any, Optional, cast
import pytest

@pytest.fixture
def toml_string() -> str:
    return r"""
[copy]
dest.dir = "/var/backups"
dest.file = "somedir.tar.gz"
src = "/home/user/somedir"
options.parallel = true
"""

def _has_subkey(path: str, d: dict, /) -> bool:
    """
    Internal function: returns True if PATH is defined in D.

    >>> d = {'key': {'subkey': 5}}
    >>> _has_subkey('key/subkey', d)
    True
    """
    if not d or not (lpath := path.split('/')): return False

    END = len(lpath) - 1
    dd = d.copy()
    res = False

    for i, key in enumerate(lpath):
        val = dd.get(key)
        if i == END and val is not None:
            res = True
        else:
            if not isinstance(val, dict):
                break
            dd = cast(dict, val)

    return res

def test_toml_string(toml_string: str) -> None:
    data = read_toml_string(toml_string)
    copysec: dict[str, Any] = data.get('copy', {})
    assert copysec, "empty dictionary"
    assert _has_subkey('dest/dir', copysec), "unknown key 'dest/dir'"
    assert _has_subkey('dest/file', copysec), "unknown key 'dest/file'"
    assert _has_subkey('src', copysec), "unknown key 'src'"
    assert _has_subkey('options/parallel', copysec), "unknown key 'options/parallel'"

def test_toml_file(toml_string: str) -> None:
    from pathlib import Path
    
    with NamedTemporaryFile(delete=False) as fd:
        b = toml_string.encode('UTF-8')
        fd.write(b)
        tmpfile = Path(fd.name)

    data = read_toml_file(str(tmpfile))
    tmpfile.unlink()

    copysec: dict[str, Any] = data.get('copy', {})
    assert copysec, "empty dictionary"
    assert _has_subkey('dest/dir', copysec), "unknown key 'dest/dir'"
    assert _has_subkey('dest/file', copysec), "unknown key 'dest/file'"
    assert _has_subkey('src', copysec), "unknown key 'src'"
    assert _has_subkey('options/parallel', copysec), "unknown key 'options/parallel'"
