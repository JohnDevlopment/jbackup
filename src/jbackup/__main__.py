# Main script

from argparse import ArgumentParser, Namespace
from . import (ListAvailableActionsAction, ListAvailableRulesAction,
               ShowPathAction, ListLoglevelsAction, get_data_path)
from typing import NoReturn, Callable
from .logging import get_logger
import sys

def exit_with_code(f: Callable[[Namespace], int | None]) -> Callable[[Namespace], int]:
    def inner(args: Namespace):
        code: int | None = f(args)
        return code or 0

    return inner

@exit_with_code
def create_action(args: Namespace) -> int:
    """Function for subcommand 'create-action'."""
    from .template import write_action_file
    from .utils import DirectoryNotEmptyError, DirectoryNotFoundError

    logger = get_logger('')

    action: str = args.ACTION
    logger.debug("creating action '%s'", action)

    datapath = get_data_path()
    logger.debug("set data path to %s", datapath)

    actionfile = ""
    try:
        actionfile = write_action_file(datapath / 'actions' / action)
    except DirectoryNotFoundError as exc:
        logger.error("'%s' does not exist", exc.directory)
    except DirectoryNotEmptyError as exc:
        logger.error("failed writing to %s. contains %s", exc, ", ".join(exc.files))

    if not actionfile: return 1

    logger.info("written action to %s", actionfile)

    return 0

def create_rule(args: Namespace) -> NoReturn:
    """Function for subcommand 'create-rule'."""
    raise NotImplementedError('create_rule')

def edit_action(args: Namespace) -> NoReturn:
    """Function for subcommand 'edit-action'."""
    raise NotImplementedError('edit_action')

def edit_rule(args: Namespace) -> NoReturn:
    """Function for subcommand 'edit-rule'."""
    raise NotImplementedError('edit_rule')

def do(args: Namespace) -> NoReturn:
    """Evaluates one of the actions with one or more rules."""
    raise NotImplementedError('do')

def run():
    parser = ArgumentParser(prog='jbackup')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--list-actions', action=ListAvailableActionsAction)
    group.add_argument('--list-rules', action=ListAvailableRulesAction)
    group.add_argument('--path', action=ShowPathAction)
    group.add_argument('--levels', action=ListLoglevelsAction)

    subparsers = parser.add_subparsers(dest='subcommand', title='subcommands', required=True)

    # 'create/edit-action/rule' subcommands
    gbls = globals()

    for name in ('create-action', 'create-rule', 'edit-action', 'edit-rule'):
        func = gbls[name.replace('-', '_')]
        subparser_x = subparsers.add_parser(name)
        subparser_x.set_defaults(func=func)

        i = name.index('-')
        dowhat = name[0:i]
        thing = name[i+1:]
        subparser_x.add_argument(thing.upper(), help=f"name of the new {thing} to {dowhat}")

    # 'do' subcommand
    subparser_do = subparsers.add_parser('do', description='Run a action on one or more rules')
    subparser_do.add_argument('ACTION', help='action to be done')
    subparser_do.add_argument('RULE', nargs='+', help='rules to apply to ACTION')

    args = parser.parse_args()
    func = args.func
    return func(args)

if __name__ == "__main__":
    code = run()
    if isinstance(code, int):
        sys.exit(code)
