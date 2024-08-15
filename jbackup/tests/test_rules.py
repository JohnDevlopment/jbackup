# pylint: disable=missing-function-docstring

from __future__ import annotations
from contextlib import contextmanager
from pathlib import Path
from typing import Any, TypeAlias

from jbackup.rules.exceptions import MissingOptionError

from ..rules import Rule
from ..types import StrPath

import pytest

AnyDict: TypeAlias = dict[str, Any]

@contextmanager
def delete_after(fp: str | StrPath):
    fp = Path(fp)
    yield fp
    fp.unlink(True)

@pytest.fixture(scope="class")
def rule_dict() -> AnyDict:
    return {
        'compress': {
            'verbose': False,
            'archive': "/var/backups/user/my-repo.tar.gz",
            'source': "~/my-repo",
            'extraOptions': {
                'compressionProgram': ""
            },
        },
    }

@pytest.fixture(scope="class")
def rule_string():
    return \
        '''[compress]
verbose = false
archive = "/var/backups/user/my-repo.tar.gz"
source = "~/my-repo"
extraOptions = { compressionProgram = "" }
'''

def test_read_rule(rule_string: str, tmp_path: Path):
    fp = tmp_path / "rule.toml"
    fp.write_text(rule_string)

    rule = Rule(str(fp), mode='r')

    # Assert that certain keys are defined
    value = rule['compress/verbose']
    assert value is False
    value = rule['compress/archive']
    assert value == "/var/backups/user/my-repo.tar.gz"
    value = rule['compress/source']
    assert value == "~/my-repo"
    value = rule['compress/extraOptions']
    match value:
        case {'compressionProgram': prog}:
            assert prog == "", f"wrong 'compressionProgram' {prog!r}: must be ''"

        case v:
            temp = {'compressionProgram': ""}
            pytest.fail(f"invalid 'extraOptions' {v!r}: expected {temp!r}")

    # Default value
    default = []
    value = rule.get("compress/extraOptions/compressionFlags", default, True)
    assert value is default

    # Exceptions
    with pytest.raises(MissingOptionError):
        rule.get("compress/doesnotexist")

def test_write_rule(rule_dict: AnyDict, tmp_path: Path):
    fp = tmp_path / "rule.toml"
    Rule(fp, 'w', rule_dict)
    assert fp.exists()

def test_find_rule(rule_string: str, tmp_path: Path):
    with delete_after(Rule.get_path() / "example-rule.toml") as fp:
        fp.write_text(rule_string)
        Rule.find("example-rule")
        Rule.find("example-rule", True)

    with pytest.raises(FileNotFoundError):
        Rule.find("example-rule")
