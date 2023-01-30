"""Action and rule templates."""

from __future__ import annotations
from pathlib import Path
from typing import cast
from ..utils import DirectoryNotFoundError, Pathlike
from ..logging import get_logger
from ..rules import Rule
import re

TEMPLATEFILE = Path(__file__).parent / '_template.py'

assert TEMPLATEFILE.exists(), f"no {TEMPLATEFILE}"

def write_action_file(filename: str | Pathlike, action_name: str) -> str:
    """
    Writes an action script to the specified file.

    DirectoryNotFoundError is raised if the parent of
    FILENAME does not exist.

    Returns the path to the file that was written.
    """
    if isinstance(filename, str):
        filename = Path(filename)
    else:
        filename = cast(Path, filename)

    # Error if directory of file does not exist
    parent = filename.parent
    if not parent.exists() or not parent.is_dir():
        raise DirectoryNotFoundError(parent)

    # Copy test inside template file
    with TEMPLATEFILE.open('rt') as fd:
        data = fd.read()

    data = re.sub(r'(class Action_)Dummy',
                  r'\1{}'.format(action_name.capitalize()), data)

    # Write output file
    with filename.open('wt') as fd:
        fd.write(data)

    return str(filename)

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
