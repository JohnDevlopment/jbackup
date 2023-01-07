from tempfile import TemporaryFile

from ..rules.config.toml_config_adapter import TOMLFile
from ..rules import Rule
# from typing import Any
from pathlib import Path
import pytest

@pytest.fixture()
def toml_file() -> Path:
    return Path(__file__).parent / '_testrule.toml'

# class SomeTestFile:
#     def __init__(self, p: str, mode: str):
#         self.fd: Any = None
#         self.path = Path(p)
#         self.args = (p, mode)
#
#     def __enter__(self):
#         self.fd = open(*self.args)
#         return self
#
#     def __exit__(self, *args):
#         self.fd.close()
#         self.path.unlink()
#
#     @classmethod
#     def create(cls, p: str, mode: str):
#         return cls(p, mode)

def test_toml_file(toml_file: Path) -> None:
    with open(toml_file, 'rb') as fd:
        tomlf = TOMLFile(fd)

    assert '/copy' in tomlf
    assert 'copy/dest' in tomlf
    assert 'copy/dest/dir' in tomlf
    assert 'copy/dest/file' in tomlf

    assert isinstance(tomlf.get('/copy'), dict)
    assert isinstance(tomlf.get('copy/dest'), dict)
    assert isinstance(tomlf.get('copy/dest/dir'), str)
    assert isinstance(tomlf.get('copy/dest/file'), str)

def test_rule(toml_file: Path) -> None:
    rule = Rule(str(toml_file))

    val = rule['/copy']
    assert isinstance(val, dict)

    val = rule['/copy/dest']
    assert isinstance(val, dict)

    val = rule['/copy/dest/dir']
    assert isinstance(val, str)

    val = rule['/copy/dest/file']
    assert isinstance(val, str)
