from __future__ import annotations
from typing import Annotated, Any, Optional
import logging

import typer

from . import APPNAME
from .rules.rule import Rule

CONTEXT_SETTINGS: dict[str, Any] = {
    'help_option_names': ["-h", "--help"]
}

app = typer.Typer(name=APPNAME, context_settings=CONTEXT_SETTINGS)

@app.command()
def compress(
    rule: Annotated[list[str], typer.Argument(help="One or more rules.")]
) -> int:
    return 0

@app.command()
def locate(
    rule: Annotated[str, typer.Argument(help="The name of a rule to locate.")]
) -> int:
    try:
        fp = Rule.find(rule)
        print(fp)
    except FileNotFoundError:
        logging.error("Rule '%s' does not exist", rule)
        return 1

    return 0

if __name__ == '__main__':
    raise NotImplementedError
