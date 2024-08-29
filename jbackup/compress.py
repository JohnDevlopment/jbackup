from __future__ import annotations
from collections import Counter
from fnmatch import fnmatchcase
from pathlib import Path
from tarfile import open as open_tar
from typing import Any, Protocol
import logging
import re

from . import APPNAME
from .types import StrPath
from .rules import Rule
from .utils import chdir_temp

# TGZ_FILE_PATTERN = re.compile(r'\.t(?:ar\.gz|gz)$')
TAR_FILE_PATTERN = re.compile(r'\.t(?:ar(?:\.gz)?|gz)$')

class Compressor(Protocol):
    "Interface for a compressor function."

    def __call__(self, rule: Rule):
        ...

class DummyCompressor:
    def __init__(self, *args: Any) -> None:
        pass

    def add(self, file: StrPath) -> None:
        print(f"Adding {file}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

def _dir_empty(pth: Path) -> bool:
    count = Counter(pth.iterdir())
    return count.total() == 0

def _recurse_directory(dirname: StrPath, excludes: list[str], paths: list[Path] | None,
                       logger: logging.Logger) -> list[Path]:
    if paths is None:
        paths = []

    for pth in Path(dirname).iterdir():
        # We have a list of shell patterns that match paths that
        # should be excluded
        spth = str(pth)
        is_excluded = False
        for exclude in excludes:
            if fnmatchcase(spth, exclude):
                is_excluded = True
                break
        if is_excluded:
            is_excluded = False
            logger.debug("Excluding '%s'", spth)
            continue

        if pth.is_dir():
            if _dir_empty(pth):
                # Append the directory to the array and then recurse the
                # function
                logger.debug("Adding empty directory: %s", pth)
                paths.append(pth)
            else:
                _recurse_directory(pth, excludes, paths, logger)
        elif pth.is_symlink():
            # TODO: Resolve links prior to these ifs
            # Resolve symbolic links
            paths.append(pth.resolve())
        else:
            paths.append(pth)

    paths.reverse()
    return paths

def recurse_directory(dirname: StrPath, excludes: list[str]) -> list[Path]:
    return _recurse_directory(dirname, excludes, None, logging.getLogger(APPNAME))

def _dummy_print(*_: Any) -> None:
    pass

def _my_print(*args: Any) -> None:
    print(*args)

def _compress_tar(rule: Rule) -> None:
    archive: str = rule['compress/archive']
    source = Path(rule['compress/source'])

    # cd to the parent directory
    with chdir_temp(source.parent):
        source = source.name

        # Check archive's extension
        m = TAR_FILE_PATTERN.search(archive)
        assert m is not None

        # tar.gz and tar files are accepted
        mode = ""
        extension = m[0]
        if extension in (".tar.gz", ".tgz"):
            mode = "w:gz"
        elif extension == ".tar":
            mode = "w"
        else:
            raise ValueError(f"Unknown/unsupported format {Path(archive).suffix}")

        fn = _my_print if rule['compress/verbose'] else _dummy_print
        with open_tar(archive, mode) as tf:
            files = recurse_directory(source, rule.get('compress/exclude', [], True))
            for file in files:
                fn(f"Adding '{file}'")
                tf.add(file)

def _compress_dummy(rule: Rule) -> None:
    source = Path(rule['compress/source'])

    with chdir_temp(source.parent):
        source = source.name

        with DummyCompressor() as df:
            files = recurse_directory(source, rule.get('compress/exclude', [], True))
            for file in files:
                df.add(file)

def choose_compressor(filename: StrPath) -> Compressor:
    """
    Choose a compressor for FILENAME.

    Returns a function that compresses a directory or file
    according to the rules set out in RULE.

    Raises:
    * ValueError (invalid extension)
    * MissingOptionError
    * MissingSectionError
    """
    if TAR_FILE_PATTERN.search(str(filename)):
        return _compress_tar
    elif str(filename).lower() == "dummy":
        return _compress_dummy

    raise ValueError(f"Unsupported format: {Path(filename).suffix}")
