"""
Actions module.

ActionType refers to the Action type itself.
"""

from __future__ import annotations
from ..utils import LoadError, Pathlike
from .action_protocol import Action
from .params import *
from ..loader import load_module_from_file, ModuleProxy
from pathlib import Path
from typing import TYPE_CHECKING, Type, cast
import re, logging

__all__ = [
    # Classes
    'Action',
    'ActionNotLoaded',
    'ActionProperty',
    'ActionType',
    'ModuleProxy',
    'UndefinedProperty',

    # Functions
    'get_action_info',
    'get_logger',
    'load_action'
]

if TYPE_CHECKING:
    from typing import Optional

class _DocstringFormatter: # pragma: no cover
    __slots__ = ('lines', 'proplines', 'indent')

    def __init__(self, cls: ActionType, indent: int=4):
        self.indent: int = indent

        string = cls.__doc__ or ""
        if string:
            string = re.sub(r'\n[ \t]*(.+)', r'\n\1', string)
            lines: list[str] = [cast(str, line).replace('\n', ' ').strip()
                                for line in re.split(r'\n\n', string)]
        else:
            lines = []
        del string

        properties = cls.properties # pyright: ignore
        self.proplines: list[str] = []
        if properties:
            self.proplines = [str(prop) for prop in properties]

        self.lines: list[str] = lines

    @staticmethod
    def concat_string(lines: list[str], proplines: list[str], indent: int) -> str:
        space: str = " " * indent
        string = "\n\n".join([space + line for line in lines])
        if proplines:
            string += f"\n\n{space}Properties:\n\n"
            string += "\n\n".join([f"{space * 2}{line}" for line in proplines])
        return string

    def __str__(self) -> str:
        return self.concat_string(self.lines, self.proplines, 4)

class ActionNotLoaded(LoadError):
    """An error for when an action cannot be loaded."""

ActionType = Type[Action]

def get_action_info(action: ActionType) -> str: # pragma: no cover
    """Return the string documentation of an action."""
    if action.__doc__ is None:
        return ""

    fmtr = _DocstringFormatter(action)

    return str(fmtr)

def _find_action_class(module: ModuleProxy) -> Optional[ActionType]:
    res = None
    for name in dir(module):
        if name.startswith('Action_'):
            res = module[name]
            break
    return res

def get_logger(action: str) -> logging.Logger:
    """Returns a logger for the specified action."""
    logger = logging.getLogger(f'action.{action}')

    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(f"%(levelname)s %(name)s: [%(asctime)s] %(message)s"))

    logger.addHandler(sh)

    return logger

def load_action(filename: str | Pathlike, name: str) -> ActionType:
    """
    Load an action from file.

    FILENAME is a path to a Python script. NAME
    is the name of the action.

    Raise ActionNotLoaded on failure.
    """
    assert isinstance(filename, (str, Path)), "invalid type"

    # Convert FILENAME to Path
    if isinstance(filename, str):
        filepath = Path(filename)
    else:
        filepath = cast(Path, filename)

    # Load module
    module = load_module_from_file(filepath, name)

    # Find the action class
    action = _find_action_class(module)
    if action is None:
        raise ActionNotLoaded(name, "no action class found")

    return action
