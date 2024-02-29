# Reversed for the 'complete' subcommand.

from __future__ import annotations
from typing import TYPE_CHECKING
from .utils import list_available_actions, list_available_rules
from .logging import get_logger
from argparse import Action
import itertools

if TYPE_CHECKING:
    from typing import Callable, Iterable, Literal, Any
    from argparse import Namespace, ArgumentParser

class FirstArgAction(Action):
    def __init__(self, option_strings, dest, **kw):
        super().__init__(option_strings, dest, nargs=0, required=False, **kw)

    def __call__(self, parser: ArgumentParser, _namespace: Namespace, # pyright: ignore
                 _values, _option_string): # pyright: ignore
        print("create-rule create-action do show locate --list-actions --list-rules --path --levels")
        parser.exit()

def _complete(args: Namespace): # pyright: ignore
    logger = get_logger('complete', stream=True)

    comp_cword: int = args.CWORD
    commandline: list[str] = args.COMMANDLINE
    if not commandline: return 1

    logger.debug("comp_cword = %d", comp_cword)
    logger.debug("complete commandline: %s", commandline)

    # Delete certain words from the first arg
    if commandline[0] == "jbackup":
        commandline.pop(0)
        logger.debug("remove 'jbackup' from commandline")

    subcommand = commandline[0]
    logger.debug("subcommand: %s", subcommand)

    def _print_list(l: Iterable[str]) -> None:
        print(" ".join(l))

    if comp_cword < 2: return 1

    def _get(func: Callable[[Literal['system', 'user']], list[str]]) -> set[str]:
        return set(itertools.chain(func('system'), func('user')))

    comp_reply: set[str] = set()

    if subcommand == 'do':
        # Subcommand 'do'
        if comp_cword == 2:
            # Print available actions
            comp_reply = _get(list_available_actions)
        elif comp_cword > 2:
            # Print available rules
            comp_reply = _get(list_available_rules)
    elif subcommand == 'create-action':
        # Subcommand 'create-action'
        actions = _get(list_available_actions)
        cmdl = set(commandline).intersection(actions)
        if not cmdl:
            comp_reply = actions
    elif subcommand == 'create-rule':
        # Subcommand 'create-rule'
        rules = _get(list_available_rules)
        cmdl = set(commandline).intersection(rules)
        if not cmdl:
            comp_reply = rules
    elif subcommand == 'show':
        # Subcommand 'show'
        comp_reply = _get(list_available_actions)
    elif subcommand == 'locate':
        # Subcommand: 'locate'
        if "--rule" in commandline or "-r" in commandline:
            # List rules
            comp_reply = _get(list_available_rules)
        else:
            # List actions
            comp_reply = _get(list_available_actions) | {"--rule", "-r"}

    if comp_reply:
        _print_list(comp_reply)
