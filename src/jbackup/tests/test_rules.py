from ..rules.config import MissingOptionError, MissingSectionError
from ..rules.config.toml_config_adapter import TOMLFile
from ..rules import Rule, RuleParserError, parse_string
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

def test_toml_errors(tmp_path: Path):
    # Error raised for bad syntax
    f = tmp_path / 'bad.toml'
    with open(f, 'w') as fd:
        fd.write("""[invalidsection
invalidvalue =
""")

    with pytest.raises(RuleParserError):
        TOMLFile(str(f))

    # Error raised for missing section
    f = f.parent / 'section.toml'
    with open(f, 'w') as fd:
        fd.write("""[section]
key = "value"
""")

    with pytest.raises(MissingSectionError):
        tf = TOMLFile(str(f))
        tf.get('missingsection/option')

    # Error raised for invalid mode
    with pytest.raises(ValueError):
        TOMLFile('missing.toml', 'b') # pyright: ignore

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

    assert rule.get('/missing/option', safe=True) is None

    with pytest.raises(MissingOptionError):
        rule.get('/missing/option')

def test_string_parse():
    path = parse_string('@type path /home/foobar/afile.txt')
    assert issubclass(type(path), Path)

    string = parse_string('@type str /home/foobar/afile.txt')
    assert isinstance(string, str)
