# Main script

from __future__ import annotations
from argparse import ArgumentParser, Namespace
from . import (ListAvailableActionsAction, ListAvailableRulesAction,
               ShowPathAction, ListLoglevelsAction, get_data_path,
               find_rule, find_action)
from typing import Callable
from .logging import get_logger
from .rules import Rule
import sys

_SubcommandFunction = Callable[[Namespace], int]

def exit_with_code(f: Callable[[Namespace], int | None]) -> _SubcommandFunction:
    """Decorator that causes a function to return an integer status code."""
    def inner(args: Namespace) -> int:
        code: int | None = f(args)
        return code or 0
    inner.__name__ = f.__name__
    inner.__doc__ = f.__doc__

    return inner

@exit_with_code
def show(args: Namespace) -> int:
    """Function for subcommand 'show'."""
    from .actions import load_action, get_action_info

    logger = get_logger('')

    action: str = args.ACTION
    logger.debug("show action '%s'", action)

    actionfile = find_action(action)
    if actionfile is None:
        logger.error("no action called '%s' exists", action)
        return 1

    logger.info("found action class in %s", actionfile)

    cls = load_action(actionfile, action)
    docstring = get_action_info(cls)
    print(f"Information for {action}:\nLocated at {actionfile}\n{docstring}")

    return 0

@exit_with_code
def create_action(args: Namespace) -> int:
    """Function for subcommand 'create-action'."""
    from .template import write_action_file
    from .utils import DirectoryNotFoundError

    logger = get_logger('')

    action: str = args.ACTION
    logger.debug("creating action '%s'", action)

    # Choose data path
    datapath = get_data_path()
    logger.debug("set data path to %s", datapath)

    actionfile = (datapath / 'actions' / action).with_suffix('.py')

    # Error if rule file already exists
    if find_action(action) is not None:
        logger.error("%s already exists", find_action(action))
        return 1

    # Write action to file
    outfile = ""
    try:
        outfile = write_action_file(actionfile, action)
    except DirectoryNotFoundError as exc:
        logger.error("'%s' does not exist", exc.directory)

    if not outfile: return 1

    logger.info("written action to %s", outfile)

    return 0

@exit_with_code
def create_rule(args: Namespace):
    """Function for subcommand 'create-rule'."""
    from .template import write_rule_file
    from .utils import DirectoryNotFoundError

    logger = get_logger('')

    rule: str = args.RULE
    logger.debug("creating rule '%s'", rule)

    # Extension
    ext: str = '.' + args.FORMAT
    logger.debug("using format %s", args.FORMAT)

    # Choose data path
    datapath = get_data_path()
    logger.debug("set data path to %s", datapath)

    rulefile = datapath / 'rules' / (rule + ext)

    # Error if rule file already exists
    if find_rule(rule) is not None:
        logger.error("%s already exists", find_rule(rule))
        return 1

    # Write rule to file
    outfile = ""
    try:
        outfile = write_rule_file(rulefile, rule)
    except DirectoryNotFoundError as exc:
        logger.error("'%s' does not exist", exc.directory)

    if not outfile:
        logger.error("Unable to write '%s'", rulefile)
        return 1

    logger.info("written rule to %s", outfile)

    return 0

@exit_with_code
def do(args: Namespace) -> int:
    """Function for subcommand 'do'."""
    from .actions import load_action
    from . import find_rule

    logger = get_logger('')

    actionname: str = args.ACTION
    logger.debug("show action '%s'", actionname)

    # Get action file
    actionfile = find_action(actionname)
    if actionfile is None:
        logger.error("no action called '%s' exists", actionname)
        return 1

    logger.info("found action class in %s", actionfile)

    # Load action and rules
    cls = load_action(actionfile, actionname)

    rules: list[str] = args.RULE
    for name in rules:
        rulefile = find_rule(name)
        if rulefile is None:
            logger.error("this rule does not exist: %s", name)
            continue
        rule = Rule(str(rulefile))
        action = cls(rule)
        logger.debug("loaded action %s with rule %s", actionname, name)
        action.run()

    return 0

def run():
    parser = ArgumentParser(prog='jbackup')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--list-actions', action=ListAvailableActionsAction)
    group.add_argument('--list-rules', action=ListAvailableRulesAction)
    group.add_argument('--path', action=ShowPathAction)
    group.add_argument('--levels', action=ListLoglevelsAction)

    subparsers = parser.add_subparsers(dest='subcommand', title='subcommands', required=True)

    subparser_createrule = subparsers.add_parser('create-rule')

    # 'create-action/rule' subcommands
    gbls = globals()

    for name in ('create-action', 'create-rule'):
        if name == 'create-rule':
            subparser_x = subparser_createrule
        else:
            subparser_x = subparsers.add_parser(name)

        func = gbls[name.replace('-', '_')]
        subparser_x.set_defaults(func=func)

        i = name.index('-')
        dowhat = name[0:i]
        thing = name[i+1:]
        subparser_x.add_argument(thing.upper(), help=f"name of the new {thing} to {dowhat}")

    # Additional 'create-rule' options
    subparser_createrule.add_argument('-f', '--format', choices=('toml','null'),
                                      default='toml', dest='FORMAT',
                                      help='format of the rule file')

    # 'do' subcommand
    subparser_do = subparsers.add_parser('do', description='Run a action on one or more rules')
    subparser_do.add_argument('ACTION', help='action to be done')
    subparser_do.add_argument('RULE', nargs='+', help='rules to apply to ACTION')
    subparser_do.set_defaults(func=do)

    # 'show' subcommand
    subparser_show = subparsers.add_parser('show')
    subparser_show.set_defaults(func=show)
    subparser_show.add_argument('ACTION', help='the name of an action')

    # TODO: add 'locate' subcommand: shows the location of a particular action or rule

    args = parser.parse_args()
    func = args.func
    return func(args)

if __name__ == "__main__":
    code = run()
    if isinstance(code, int):
        sys.exit(code)
