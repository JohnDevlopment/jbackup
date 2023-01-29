from tempfile import TemporaryFile

from ..rules.config.toml_config_adapter import TOMLFile
from ..rules import Rule
# from typing import Any
from pathlib import Path
import pytest

@pytest.fixture()
def toml_file() -> Path:
    return Path(__file__).parent / '_testrule.toml'

def test_toml_file(toml_file: Path) -> None:
    tomlf = TOMLFile(str(toml_file))

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
