from __future__ import annotations
from pathlib import Path
from typing import Annotated, Any, Optional
import logging

from platformdirs import user_log_path
import typer

from . import APPNAME
from .rules import Rule
from .rules.template import make_rule
from .utils import eprintf
from .rules.exceptions import RuleParserError
from .logging import setup_logging
from .compress import choose_compressor, recurse_directory

CONTEXT_SETTINGS: dict[str, Any] = {
    'help_option_names': ["-h", "--help"]
}

app = typer.Typer(name=APPNAME, context_settings=CONTEXT_SETTINGS)

def _create_dir_if_not_exist(fp: Path, created_dirs: list[Path], /):
    if not fp.exists():
        fp.mkdir(parents=True)
        created_dirs.append(fp)

@app.callback()
def setup():
    created_dirs: list[Path] = []
    _create_dir_if_not_exist(user_log_path(APPNAME), created_dirs)

    setup_logging()

    logger = logging.getLogger(APPNAME)
    for d in created_dirs:
        logger.info("Created %s", d)

@app.command()
def compress(
    names: Annotated[list[str], typer.Argument(help="One or more rules.", metavar="RULE")]
) -> int:
    logger = logging.getLogger(APPNAME)

    for name in names:
        logger.debug("Using rule '%s'", name[0])
        rule = Rule.find(name, True)
        logger.debug("Loaded rule")
        compressor = choose_compressor(rule['compress/archive'])
        compressor(rule)

    return 0

@app.command()
def new(
    rule: Annotated[str, typer.Argument(help="The rule to create.")],
    source: Annotated[Optional[Path], typer.Option(help="Specify the source directory.")]=None,
    archive: Annotated[Optional[Path], typer.Option(help="Specify the archive file.")]=None,
    verbose: Annotated[bool, typer.Option("--verbose", help="Specify whether the")]=False
):
    """
    Create a new rule.

    RULE is the name of the rule to be created.
    """
    kw = dict[str, Any](verbose=verbose)
    if source is not None:
        kw['source'] = source
    if archive is not None:
        kw['archive'] = archive

    try:
        make_rule(rule, **kw)
    except FileExistsError as exc:
        eprintf("File already exists for rule %s: %s", rule, exc)
    except RuleParserError as exc:
        eprintf("Error creating rule '%s': %s", rule, exc)

    return 0

@app.command()
def locate(
    rule: Annotated[str, typer.Argument(help="The name of a rule to locate.")]
) -> int:
    """
    Print the location of a rule.
    """
    logger = logging.getLogger(APPNAME)

    try:
        logger.debug("Trying to locate rule '%s'", rule)
        fp = Rule.find(rule)
        print(fp)
    except FileNotFoundError:
        logging.error("Rule '%s' does not exist", rule)
        return 1

    return 0

if __name__ == '__main__':
    raise NotImplementedError
