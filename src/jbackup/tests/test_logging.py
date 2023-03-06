from __future__ import annotations
from ..logging import get_logger, Level
from typing import TYPE_CHECKING, Protocol
from pytest import LogCaptureFixture
import pytest

if TYPE_CHECKING:
    #from typing import Callable
    pass

class _LoggerMethod(Protocol):
    def __call__(self, msg: object, *args: object):
        pass

logger = get_logger('tests.logger', Level.DEBUG)

TESTS = [
    (logger.debug, Level.DEBUG),
    (logger.info, Level.INFO),
    (logger.warning, Level.WARN),
    (logger.error, Level.ERROR),
    (logger.critical, Level.CRITICAL)
]

@pytest.mark.parametrize("func,level", TESTS)
def test_logger(caplog: LogCaptureFixture, func: _LoggerMethod, level: Level):
    msg = "is this message seen?"
    func(msg)
    assert caplog.record_tuples == [("tests.logger", level, msg)]
