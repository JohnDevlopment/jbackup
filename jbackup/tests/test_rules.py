from tempfile import TemporaryFile

from ..rules.config.toml_config_adapter import TOMLFile
from ..rules.config import MissingSectionError, MissingOptionError
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

def test_toml_file(toml_string: str) -> None:
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
