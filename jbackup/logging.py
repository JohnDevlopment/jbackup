"""Logging module."""

from __future__ import annotations
from pathlib import Path
from typing import TYPE_CHECKING
import logging, yaml

if TYPE_CHECKING:
    from typing import Any

_Init = False

def _setup_logging() -> None:
    import logging.config

    # logging.yaml in this directory
    fp = Path(__file__).parent / 'logging.yaml'
    with open(fp, 'rt') as fd:
        LOGGING_CONFIG: dict[str, Any] = yaml.safe_load(fd)
        logging.config.dictConfig(LOGGING_CONFIG)

def get_logger(name=""):
    global _Init

    if not _Init:
        _setup_logging()
        _Init = True

    return logging.getLogger(name)
