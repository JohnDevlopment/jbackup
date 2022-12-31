from tempfile import TemporaryFile

from ..rules.config.toml_config_adapter import TOMLFile
from typing import Any
from pathlib import Path
import pytest, io

@pytest.fixture
def toml_string() -> str:
    return r"""
[copy]
dest.dir = "/var/backups"
dest.file = "somedir.tar.gz"
src = "/home/user/somedir"
options.parallel = true
"""

class TestFile:
    def __init__(self, p: str, mode: str):
        self.fd: Any = None
        self.path = Path(p)
        self.args = (p, mode)

    def __enter__(self):
        self.fd = open(*self.args)
        return self

    def __exit__(self, *args):
        self.fd.close()
        self.path.unlink()

    @classmethod
    def create(cls, p: str, mode: str):
        return cls(p, mode)

@pytest.mark.parametrize('file_is_string', (False, True))
def test_toml_file(toml_string: str, file_is_string: bool) -> None:
    if file_is_string:
        with open('file.toml', 'w') as fd:
            fd.write(toml_string)

        with TestFile.create('file.toml', 'rb') as f:
            tomlf = TOMLFile(f.fd)
    else:
        with TemporaryFile('w+b') as fd:
            data = toml_string.encode('UTF-8')
            fd.write(data)
            fd.seek(0)
            tomlf = TOMLFile(fd)

    assert '/copy' in tomlf
    assert 'copy/dest' in tomlf
    assert 'copy/dest/dir' in tomlf
    assert 'copy/dest/file' in tomlf

    assert isinstance(tomlf.get('/copy'), dict)
    assert isinstance(tomlf.get('copy/dest'), dict)
    assert isinstance(tomlf.get('copy/dest/dir'), str)
    assert isinstance(tomlf.get('copy/dest/file'), str)
