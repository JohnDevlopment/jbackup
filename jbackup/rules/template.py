# pylint: disable=missing-module-docstring
from __future__ import annotations
from pathlib import Path
import logging

from ..types import StrPath
from ..exceptions import OSErrorFactory
from .config.config_protocol import ConfigString
from .config.toml_config_adapter import TOMLFileString
from .rule import Rule

def make_rule(name: str, *, verbose: bool=False, archive: StrPath="archive.tar.gz",
              source: StrPath=""):
    def _absolute(f: StrPath):
        return str(Path(f).absolute())

    dct = {
        'compress': {
            'verbose': verbose,
            'archive': _absolute(archive),
            'source': _absolute(source),
        },
    }

    fp = Rule.get_path() / f"{name}.toml"
    if fp.exists():
        raise OSErrorFactory.FileExistsError(fp)

    Rule(fp, 'w', dct)
    logging.info("Wrote '%s'", fp)
