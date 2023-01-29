"""Action and rule templates."""

from __future__ import annotations
from pathlib import Path
from typing import cast
from ..utils import DirectoryNotFoundError, DirectoryNotEmptyError, Pathlike
from ..logging import get_logger
from ..rules import Rule

TEMPLATEFILE = Path(__file__).parent / '_template.py'

assert TEMPLATEFILE.exists(), f"no {TEMPLATEFILE}"

def write_action_file(directory: str | Pathlike) -> str:
    """
    Writes an action script to the specified directory.

    DirectoryNotFoundError is raised if the parent of
    DIRECTORY does not exist.

    DirectoryNotEmptyError is raised if DIRECTORY
    contains .py files.

    DIRECTORY is created if it does not exist.

    Returns the path to the file that was written.
    """
    if isinstance(directory, str):
        directory = Path(directory)
    else:
        directory = cast(Path, directory)

    parent = directory.parent

    if not parent.exists():
        raise DirectoryNotFoundError(parent)

    if not directory.exists():
        directory.mkdir()

    # Error if python files exist in directory
    files = [str(f) for f in directory.glob('*.py')]
    if files:
        raise DirectoryNotEmptyError(str(directory), files=files)

    with TEMPLATEFILE.open('rt') as fd:
        data = fd.read()

    # Write output file
    outfile = Path(directory) / 'action.py'
    with outfile.open('wt') as fd:
        fd.write(data)

    return str(outfile)

def write_rule_file(filename: str | Pathlike, rulename: str) -> str:
    """Write a rule file with the specified name."""
    logger = get_logger('io.rules')

    if isinstance(filename, str):
        filename = Path(filename)
    elif not isinstance(filename, Path):
        filename = Path(str(filename))

    parent = filename.parent
    logger.debug("%s (located in %s)", filename.name, parent)
    if not parent.exists():
        raise DirectoryNotFoundError(parent)

    rule = Rule(str(filename), 'w')

    return str(filename)
