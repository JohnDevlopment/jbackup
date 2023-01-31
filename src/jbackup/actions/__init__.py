"""
Actions module.

ActionType refers to the Action type itself.
"""

from ..utils import LoadError, Pathlike
from .action_protocol import Action
from .params import *
from ..loader import load_module_from_file, ModuleProxy
from pathlib import Path
from typing import Optional, Type, cast

__all__ = [
    # Classes
    'Action',
    'ActionNotLoaded',
    'ActionProperty',
    'ActionType',
    'ModuleProxy',

    # Functions
    'load_action'
]

class ActionNotLoaded(LoadError):
    """An error for when an action cannot be loaded."""

ActionType = Type[Action]

def _find_action_class(module: ModuleProxy) -> Optional[ActionType]:
    res = None
    for name in dir(module):
        if name.startswith('Action_'):
            res = module[name]
            break
    return res

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
