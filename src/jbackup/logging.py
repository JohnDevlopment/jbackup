"""Logging module."""

from enum import IntEnum, auto
from .utils import get_env, DataDescriptor
from typing import cast

class Level(IntEnum):
    """Logging level."""

    DEBUG = auto()
    INFO = auto()
    WARN = auto()
    ERROR = auto()
    CRITICAL = auto()

class _LevelConv:
    def __new__(cls, value: str | int):
        value = int(value)
        try:
            return Level(value)
        except ValueError:
            pass
        return Level.INFO

DEFAULT_LEVEL = Level(get_env('JBACKUP_LEVEL', Level.INFO.value, type_=_LevelConv))

class Logger:
    """
    A logger representing a single logging channel.

    A "logging channel" indicates an area of an
    application. What an area is is up to the
    programmer.

    Loggers have unique names that follow the syntax
    of Python namespaces. That is to say, names are
    compose of levels separated by periods. For
    example, "input", "input.gui".
    """

    name = DataDescriptor('', doc="Logger's unique identifier.", frozen=True)
    level = DataDescriptor(Level.INFO, doc="Severity level.")

    def __init__(self, name: str, level: Level):
        self.name = name
        self.level = level

    def _print(self, msg: str, level: Level) -> bool:
        if self.enabled(level):
            print(f"{level.name}: {msg}")
            return True
        return False

    def enabled(self, level: Level) -> bool:
        """Return true if enabled for the specified level."""
        return int(level) >= self.level

    # Functions to print

    def warn(self, msg: str, *args) -> None:
        """Print a message on severity level WARN."""
        self._print(msg % args, Level.WARN)

    def error(self, msg: str, *args) -> None:
        """Print a message on severity level ERROR."""
        self._print(msg % args, Level.ERROR)

    def debug(self, msg: str, *args) -> None:
        """Print a message on severity level DEBUG."""
        self._print(msg % args, Level.DEBUG)

    def critical(self, msg: str, *args) -> None:
        """Print a message on severity level CRITICAL."""
        self._print(msg % args, Level.CRITICAL)

    def info(self, msg: str, *args) -> None:
        """Print a message on severity level INFO."""
        self._print(msg % args, Level.INFO)

_Cache: dict[str, Logger] = {}

def get_logger(name: str, level: Level=Level(DEFAULT_LEVEL)) -> Logger:
    """
    Return a logger object with the specified NAME, creating it if necessary.

    The returned logger is cached based off of NAME, so
    subsequent calls with the same NAME will return the
    same logger.
    """
    global _Cache

    logger = _Cache.get(name)
    if logger is None:
        logger = Logger(name, level)
    else:
        logger.level = level

    return logger
