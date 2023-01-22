"""
Action and rule templates.


"""

from __future__ import annotations
from pathlib import Path
from typing import cast
from ..utils import DirectoryNotFoundError, DirectoryNotEmptyError, Pathlike

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
