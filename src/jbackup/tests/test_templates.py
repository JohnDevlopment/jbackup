from tempfile import TemporaryDirectory
from ..template import write_action_file, write_rule_file
from ..utils import *
from pathlib import Path
import pytest, os.path as path, io

class TestWriteAction:
    def test_write_action(self, tmp_path: Path):
        # Write action file and look for the Action class
        actionfile = write_action_file(tmp_path / 'action.py', 'action')
        with open(actionfile, 'rt') as fd:
            data = fd.read()
        with io.StringIO(data) as fd:
            fd.seek(data.find('class'))
            line = fd.readline()
        assert line.startswith("class Action")

    def test_errors(self):
        d = Path('/does/not/exist')
        assert not d.exists()
        with pytest.raises(DirectoryNotFoundError):
            actionfile = write_action_file(d / 'action.py', 'action')

class TestWriteRule:
    def test_write_rule(self, tmp_path: Path):
        from ..utils import Pathlike
        rulefile = write_rule_file(tmp_path / 'rule.toml', 'rule')
        assert rulefile, f"{tmp_path / 'rule.toml'} not written"
