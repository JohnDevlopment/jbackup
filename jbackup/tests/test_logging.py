from __future__ import annotations
from ..logging import get_logger, Level, add_handler, get_record_tuple
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
add_handler(logger, 'stack')

TESTS = [
    (logger.debug, Level.DEBUG),
    (logger.info, Level.INFO),
    (logger.warning, Level.WARN),
    (logger.error, Level.ERROR),
    (logger.critical, Level.CRITICAL)
]

@pytest.mark.parametrize("func,level", TESTS)
def test_logger(func: _LoggerMethod, level: Level):
    msg = "is this message seen?"
    func(msg)
    assert get_record_tuple(logger) == ('tests.logger', level, msg)
