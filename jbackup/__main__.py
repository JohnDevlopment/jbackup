# Main script

from argparse import ArgumentParser
from . import ListAvailableActionsAction

def run():
    parser = ArgumentParser(prog='jbackup')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--list-actions', action=ListAvailableActionsAction)
    group.add_argument('--list-rules', help='list available rules')

    parser.add_argument('ACTION', help='action to be done')
    parser.add_argument('RULE', nargs='+', help='rules to apply to ACTION')

    args = parser.parse_args()

if __name__ == "__main__":
    run()
