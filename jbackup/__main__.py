# Main script

from argparse import ArgumentParser, Namespace
from . import ListAvailableActionsAction, ListAvailableRulesAction
from typing import NoReturn

def create_action(args: Namespace) -> NoReturn:
    """Function for subcommand 'create-action'."""
    raise NotImplementedError('create_action')

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
    run()
