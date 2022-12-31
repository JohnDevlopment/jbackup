"""Logging module."""

from typing import Protocol, Any, Optional
from enum import IntEnum, auto
import logging, os

class Level(IntEnum):
    """Logging level."""

    DEBUG = auto()
    INFO = auto()
    WARN = auto()
    ERROR = auto()
    CRITICAL = auto()

level: int = int(os.environ.get('JBACKUP_LEVEL') or 0)

class Logger:
    """Logger proxy object."""

    def __init__(self, name, level=0):
        self._logger = logging.Logger(name, level)

    def warn(self, msg: str, *args, **kw):
        self._logger.warning(msg, *args, **kw)

    def error(self, msg: str, *args, **kw):
        self._logger.error(msg, *args, **kw)

    def debug(self, msg: str, *args, **kw):
        self._logger.debug(msg, *args, **kw)

    def critical(self, msg: str, *args, **kw):
        self._logger.critical(msg, *args, **kw)

    def info(self, msg: str, *args, **kw):
        self._logger.info(msg, *args, **kw)

def new_logger(name: str, level: int | Level=0) -> Logger:
    """
    Returns a new logger instance.

    The returned logger will follow the LoggerType
    protocol, defined above.
    """
    level_conv = {
        Level.DEBUG.value: logging.DEBUG,
        Level.INFO.value: logging.INFO,
        Level.WARN.value: logging.WARN,
        Level.ERROR.value: logging.ERROR,
        Level.CRITICAL.value: logging.CRITICAL
    }

    if isinstance(level, Level):
        level = level.value

    return Logger(name, level_conv[level])
