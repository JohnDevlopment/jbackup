# Extendable backup system.

import argparse, sys as _sys
from pathlib import Path
from .actions import list_actions
from .rules import list_rules

VERSION = '0.1'
ROOTDIR = Path(__file__).parent
CONFIGPATH = Path.home() / ".config" / "jbackup"

class ListAvailableAction(argparse.Action):
    INDENT = "  "

    def __init__(self,
                 option_strings,
                 dest,
                 _type: str,
                 values: list,
                 **kw):
        super().__init__(option_strings, dest, **kw)
        self.__type = _type
        self.__dirs = values

    def __call__(self, parser, namespace, values, option_string, *, msg: str):
        formatter = parser._get_formatter()
        msg += "\n%s\n" % "\n".join([self.INDENT + x for x in self.__dirs])
        formatter.add_text(msg)
        parser._print_message(msg, _sys.stdout)
        parser.exit()

class ListAvailableActionsAction(ListAvailableAction):
    def __init__(self, option_strings, dest, default=None, nargs=0,
                 required=False, **kw):
        super().__init__(option_strings, dest, _type='actions',
                         nargs=nargs, default=default, required=required,
                         values=list_actions(CONFIGPATH),
                         help='list available actions and exit', **kw)

    def __call__(self, parser, namespace, values, option_string=None):
        super().__call__(parser, namespace, values, option_string,
                         msg="Available actions:")

class ListAvailableRulesAction(ListAvailableAction):
    def __init__(self, option_strings, dest, default=None, nargs=0,
                 required=False, **kw):
        super().__init__(option_strings, dest, _type='rules',
                         nargs=nargs, default=default, required=required,
                         values=list_rules(CONFIGPATH),
                         help='list available rules and exit', **kw)

    def __call__(self, parser, namespace, values, option_string=None):
        super().__call__(parser, namespace, values, option_string,
                         msg="Available rules:")
