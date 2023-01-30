from tempfile import TemporaryDirectory
from ..template import write_action_file, write_rule_file
from ..utils import *
from pathlib import Path
import pytest, os.path as path, io

class TestWriteAction:
    def test_write_action(self):
        with TemporaryDirectory() as tmpdir:
            write_action_file(tmpdir)
            with open(path.join(tmpdir, 'action.py'), 'rt') as fd:
                data = fd.read()

            with io.StringIO(data) as fd:
                fd.seek(data.find('class'))
                line = fd.readline()

        assert line.startswith("class Action")

    def test_errors(self, tmp_path: Path):
        with pytest.raises(DirectoryNotFoundError):
            write_action_file('/does/not/exist')

        d = tmp_path / 'sub'
        write_action_file(d)

class TestWriteRule:
    def test_write_rule(self, tmp_path: Path):
        from ..utils import Pathlike
        rulefile = write_rule_file(tmp_path / 'rule.toml', 'rule')
        assert rulefile, f"{tmp_path / 'rule.toml'} not written"
