"""
Extendable backup system.

Environment Variables:
  * JBACKUP_LEVEL = logging level
"""

from __future__ import annotations
from pathlib import Path
import argparse, sys as _sys, functools
from .logging import _init_root_logger

__version__ = '1.0-alpha2'
__author__ = 'John Russell'

DATAPATHS = {
    'system': Path('/usr/local/etc/jbackup'),
    'user': Path('~/.local/etc/jbackup').expanduser()
}

@functools.cache
def _find_file_by_stem(subdir: str, name: str) -> Path | None:
    def _check(root: Path) -> Path | None:
        _dir = root / subdir
        for _file in _dir.glob("*.*"):
            if _file.stem == name:
                return _file

    res = _check(DATAPATHS['system'])
    if res: return res

    res = _check(DATAPATHS['user'])
    if res: return res

    return res

def find_rule(name: str) -> Path | None:
    """
    Find a rule with the given name.

    Returns a path if successful, or None
    upon failure.
    """
    return _find_file_by_stem('rules', name)

def find_action(name: str) -> Path | None:
    """
    Find an action with the given name.

    Returns a path if successful, or None
    upon failure.
    """
    return _find_file_by_stem('actions', name)

def list_files(subdir: str, glob: str) -> list[str]:
    res: list[str] = []

    for k in ('system', 'user'):
        _dir = DATAPATHS[k] / subdir
        res.append(k)
        res.extend(
            [f"  {x.stem}" for x in _dir.glob(glob)])

    return res

list_actions = functools.partial(list_files, 'actions', '*.py')
list_rules = functools.partial(list_files, 'rules', '*.*')

def list_loglevels() -> list[str]: # pragma: no cover
    from .logging import Level
    return ["%s: %d" % (level, level.value) for level in Level]

class ShowPathAction(argparse.Action):
    INDENT = "  "

    def __init__(self, option_strings, dest,
                 nargs=0, const=None, required=False,
                 help='list the data paths and exit',
                 **kw):
        super().__init__(option_strings, dest,
                         nargs=nargs, const=const,
                         help=help, required=required, **kw)
        self.__paths = [f"  {k}: {v}" for k, v in DATAPATHS.items()]

    def __call__(self, parser: argparse.ArgumentParser,
                 namespace: argparse.Namespace, # pyright: ignore
                 values, option_string: str): # pyright: ignore
        formatter = parser._get_formatter()
        msg = "Path:\n%s\n" % "\n".join(
            [self.INDENT + str(x) for x in self.__paths])
        formatter.add_text(msg)
        parser._print_message(msg, _sys.stdout)
        parser.exit()

class ListAvailableAction(argparse.Action): # pragma: no cover
    INDENT = "  "

    def __init__(self,
                 option_strings,
                 dest,
                 _type: str,
                 values: list,
                 **kw):
        super().__init__(option_strings, dest, **kw)
        self.__type = _type # pyright: ignore
        self.__dirs = values

    def __call__(self, parser, namespace, values, option_string, *, msg: str): # pyright: ignore
        formatter = parser._get_formatter()
        msg += "\n%s\n" % "\n".join([self.INDENT + x for x in self.__dirs])
        formatter.add_text(msg)
        parser._print_message(msg, _sys.stdout)
        parser.exit()

class ListLoglevelsAction(ListAvailableAction):
    def __init__(self, option_strings, dest, default=None, nargs=0,
                 required=False, **kw):
        super().__init__(option_strings, dest, _type='log levels',
                         nargs=nargs, default=default, required=required,
                         values=list_loglevels(),
                         help='list available actions and exit', **kw)

    def __call__(self, parser, namespace, values, option_string=None):
        super().__call__(parser, namespace, values, option_string,
                         msg="Available actions:")

class ListAvailableActionsAction(ListAvailableAction):
    def __init__(self, option_strings, dest, default=None, nargs=0,
                 required=False, **kw):
        super().__init__(option_strings, dest, _type='actions',
                         nargs=nargs, default=default, required=required,
                         values=list_actions(),
                         help='list available actions and exit', **kw)

    def __call__(self, parser, namespace, values, option_string=None):
        super().__call__(parser, namespace, values, option_string,
                         msg="Available actions:")

class ListAvailableRulesAction(ListAvailableAction): # pragma: no cover
    def __init__(self, option_strings, dest, default=None, nargs=0,
                 required=False, **kw):
        super().__init__(option_strings, dest, _type='rules',
                         nargs=nargs, default=default, required=required,
                         values=list_rules(),
                         help='list available rules and exit', **kw)

    def __call__(self, parser, namespace, values, option_string=None):
        super().__call__(parser, namespace, values, option_string,
                         msg="Available rules:")

def get_data_path() -> Path:
    """Return the data path appropriate to the user."""

    datapath: Path = DATAPATHS['system']

    f = datapath.parent / 'tmpjbackuproottest'
    try:
        with f.open('w') as fd:
            fd.write('...')
        f.unlink()
    except PermissionError:
        datapath = DATAPATHS['user']

    return datapath

_init_root_logger()
