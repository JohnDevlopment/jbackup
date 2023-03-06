"""Logging module."""
from __future__ import annotations
from typing import TYPE_CHECKING, cast

from .utils import get_env
from enum import IntEnum
import logging

class Level(IntEnum):
    """Logging level."""

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARN = logging.WARN
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

DEFAULT_LEVEL = Level(get_env('JBACKUP_LEVEL', Level.INFO, type_=int))

def get_stream_logger(name: str, level: Level=DEFAULT_LEVEL) -> logging.Logger:
    ...

def get_logger(name: str, level: Level=DEFAULT_LEVEL) -> logging.Logger:
    """
    Returns a logger with the specified NAME.

    The LEVEL dictates the severity level
    of the logger. Unless it is specified,
    it defaults to the value of JBACKUP_LEVEL
    if defined, or Level.INFO otherwise.
    """
    logger = logging.getLogger(name)

    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(f"%(levelname)s %(name)s: [%(asctime)s] %(message)s"))

    logger.addHandler(sh)
    if level is not None:
        logger.setLevel(level)

    return logger
