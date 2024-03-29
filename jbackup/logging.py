"""Logging module."""
from __future__ import annotations
from typing import TYPE_CHECKING
from .utils import get_env, Stack, DebugWarning
from enum import IntEnum
import logging, warnings

if TYPE_CHECKING:
    from typing import Literal, Any, Callable

class Level(IntEnum):
    """Logging level."""

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARN = logging.WARN
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

if __debug__:
    class _StackHandler(logging.Handler):
        """A handler that keeps a database of records."""

        def __init__(self, logger: Logger, level: Level | None=None, limit: int=10):
            super().__init__(level or Level.WARN)
            assert limit > 0
            self.limit = limit
            self._logger = logger
            self._records: Stack[logging.LogRecord] = Stack()

            setattr(logger, 'get_record', self.get_record)

        def close(self) -> None: # pragma: no cover
            self._records = Stack()
            super().close()

        def emit(self, record) -> None:
            self._records.push(record)

        def get_record(self) -> logging.LogRecord:
            return self._records.pop()

DEFAULT_LEVEL = Level(get_env('JBACKUP_LEVEL', Level.INFO, type_=int))
Logger = logging.Logger

_rootLogger: Logger

def _init_root_logger(): # pyright: ignore
    global _rootLogger
    _rootLogger = get_logger('jbackup')
    add_handler(_rootLogger, 'null')
    warnings.filterwarnings('once', category=DebugWarning)

def add_handler(logger: Logger, kind: Literal['stream', 'file', 'stack', 'null'], **kw):
    """
    Add the specified type of handler to LOGGER.

    The keyword arguments depend on what KIND of handler to add.

    stream:
      * stream = the stream to output to. should be derived from IO.
                 if omitted, defaults to sys.stderr

    file:
      * mode = same as the mode argument in open()
      * encoding = same as the encoding argumet in open()

    stack:
      * limit = size limit for the record stack

    null:
      none
    """
    hdl = None
    formatter = logging.Formatter(f"%(levelname)s %(name)s: [%(asctime)s] %(message)s")

    if kind == 'stream':
        hdl = logging.StreamHandler(kw.get('stream'))
        hdl.setFormatter(formatter)
    elif kind == 'file':
        filehdl_args: tuple[str, str | None] = (kw.get('mode', 'wt'), kw.get('encoding'))
        hdl = logging.FileHandler(kw['file'], *filehdl_args)
        hdl.setFormatter(formatter)
    elif kind == 'stack':
        if __debug__:
            stackhdl_args: list[Any] = []
            limit: int = kw.get('limit', -1)
            if limit > 0:
                stackhdl_args.append(limit)

            hdl = _StackHandler(logger, Level(logger.level), *stackhdl_args)

        if not __debug__:
            warnings.warn("stack handlers are only available in debug mode", DebugWarning)
    elif kind == 'null':
        hdl = logging.NullHandler(logger.level)

    assert hdl is not None
    logger.addHandler(hdl)

def get_logger(name: str="", level: Level=DEFAULT_LEVEL, stream: bool=False) -> Logger:
    """
    Returns a logger with the specified NAME.

    If NAME is omitted or set to an empty string
    or is "jbackup", the root logger for this
    library is returned.

    Any logger returned by this is part of the
    JBackup logger hierchy. That is to say, a
    logger named `io` is a direct child of
    the root logger. And `io.read` is a direct
    descendent of `io`, which is a descendent
    of the root logger.

    The LEVEL dictates the severity level
    of the logger. Unless it is specified,
    it defaults to the value of JBACKUP_LEVEL
    if defined, or Level.INFO otherwise.
    """
    # Return the root logger if name is "" or "jbackup"
    parts = name.split(".")
    isroot = parts[0] == "" and len(parts) == 1
    if isroot: return _rootLogger

    if parts[0] not in ("", "jbackup"):
        parts.insert(0, "jbackup")

    if parts[0] == "":
        parts[0] = "jbackup"

    name = ".".join(parts)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if stream: # pragma: no cover
        add_handler(logger, 'stream')

    return logger

if __debug__:
    def get_record_tuple(logger: Logger) -> tuple[str, int, str]:
        """
        Return a record tuple from LOGGER.

        LOGGER must have been fitted with a StackHandler,
        otherwise the outcome is undefined.

        Returns a tuple with the name of the logger, the
        level number, and the record message.
        """
        fn: Callable[..., logging.LogRecord] = getattr(logger, 'get_record')
        record = fn()
        return record.name.removeprefix("jbackup."), record.levelno, record.msg
