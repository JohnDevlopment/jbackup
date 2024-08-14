from __future__ import annotations
from pathlib import Path
from typing import Annotated, Any, Optional
import logging

import typer

from . import APPNAME
from .rules import Rule
from .rules.template import make_rule

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
def new(
    rule: Annotated[str, typer.Argument(help="The rule to create.")],
    source: Annotated[Optional[Path], typer.Option(help="Specify the source directory.")]=None,
    archive: Annotated[Optional[Path], typer.Option(help="Specify the archive file.")]=None,
    verbose: Annotated[bool, typer.Option("--verbose", help="Specify whether the")]=False
):
    kw = dict[str, Any](verbose=verbose)
    if source is not None:
        kw['source'] = source
    if archive is not None:
        kw['archive'] = archive

    make_rule(rule, **kw)
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
