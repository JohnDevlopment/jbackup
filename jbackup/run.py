from __future__ import annotations
from pathlib import Path
from typing import Annotated, Any, Optional
import logging

from platformdirs import user_log_dir, user_log_path
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

### Autocomplete functions

def _autocomplete_rule(incomplete: str):
    rules = Rule.list_rules()
    completion = [
        fp.stem for fp in rules if fp.stem.startswith(incomplete)
    ]
    return completion

### Callbacks

def _callback_list_rules(value: bool):
    if value:
        for rule in Rule.list_rules():
            print(rule)
        raise typer.Exit()

def _callback_get_log_path(value: bool):
    if value:
        print(user_log_dir(APPNAME))
        raise typer.Exit()

@app.callback()
def setup(
    list_rules: Annotated[
        bool,
        typer.Option("--list-rules", is_eager=True, help="List available rules.",
                     callback=_callback_list_rules)
    ]=False,
    get_log_path: Annotated[
        bool,
        typer.Option("--get-log-path", help="Print the log path.",
                     callback=_callback_get_log_path, is_eager=True)
    ]=False
):
    created_dirs: list[Path] = []
    _create_dir_if_not_exist(user_log_path(APPNAME), created_dirs)

    setup_logging()

    logger = logging.getLogger(APPNAME)
    for d in created_dirs:
        logger.info("Created %s", d)

###

@app.command()
def compress(
    names: Annotated[list[str], typer.Argument(help="One or more rules.", metavar="RULE",
                     autocompletion=_autocomplete_rule)]
) -> int:
    """
    Compress a repository.
    """
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
    source: Annotated[
        Optional[Path],
        typer.Option(help="Specify the source directory.", show_default=False)
    ]=None,
    archive: Annotated[
        Optional[Path],
        typer.Option(help="Specify the archive file.", show_default=False)
    ]=None,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", help="Set the rule to be verbose.",
                     show_default=False)
    ]=False,
    exclude: Annotated[
        list[str],
        typer.Option("--exclude", "-x", default_factory=list, show_default=False,
                     help="Exclude a pattern.")
    ]=...
):
    """
    Create a new rule.

    RULE is the name of the rule to be created.

    To exclude a pattern, pass `--exclude <pattern>`, where
    `<pattern>` is a shell pattern to match against the absolute
    path of each file/directory being processed. To pass
    multiple patterns, repeat this option that many times, as
    in: `--exclude '*.pyc' --exclude '__pycache__/*`.
    """
    assert isinstance(exclude, list)

    kw = dict[str, Any](verbose=verbose)
    if source is not None:
        kw['source'] = source
    if archive is not None:
        kw['archive'] = archive
    if exclude is not None:
        kw['exclude'] = exclude

    try:
        make_rule(rule, **kw)
    except FileExistsError as exc:
        eprintf("File already exists for rule %s: %s", rule, exc)
    except RuleParserError as exc:
        eprintf("Error creating rule '%s': %s", rule, exc)

    return 0

@app.command()
def locate(
    rule: Annotated[
        str,
        typer.Argument(help="The name of a rule to locate.", autocompletion=_autocomplete_rule)
    ]
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
