from __future__ import annotations
from pathlib import Path
import subprocess as sp

import pytest

from ..compress import recurse_directory
from ..types import StrPath

def mkdir(*dirs: StrPath, base: StrPath, parents: bool=False, exists_ok: bool=False):
    base = Path(base)

    for d in dirs:
        d = base / Path(d)
        d.mkdir(parents=parents, exist_ok=exists_ok)

def test_recursion(tmp_path: Path):
    mkdir("dir1", "dir1/sdir1", "dir2", "dir2/sdir1", base=tmp_path)

    dirs = recurse_directory(tmp_path)
    match dirs:
        case [d1, d2, d3, d4]:
            assert str(d1).endswith("/dir1/sdir1"), f"'{d4}' does not end with '/dir2/sdir1'"
            assert str(d2).endswith("/dir1"), f"'{d3}' does not end with '/dir2'"
            assert str(d3).endswith("/dir2/sdir1"), f"'{d2}' does not end with '/dir1/sdir1'"
            assert str(d4).endswith("/dir2"), f"'{d1}' does not end with '/dir1'"

        case _:
            pytest.fail("recurse_directory() did not return 4-element list")
