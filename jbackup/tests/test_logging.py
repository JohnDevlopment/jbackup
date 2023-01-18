from ..logging import get_logger, Level
from typing import NamedTuple

class CaptureResult(NamedTuple):
    out: str
    err: str

def test_logger(capsys):
    logger = get_logger('tests.logging', Level.DEBUG)

    logger.debug("See this message?")
    captured: CaptureResult = capsys.readouterr()
    assert captured.out.startswith("DEBUG")

    logger.info("See this message?")
    captured: CaptureResult = capsys.readouterr()
    assert captured.out.startswith("INFO")

    logger.warn("See this message?")
    captured: CaptureResult = capsys.readouterr()
    assert captured.out.startswith("WARN")

    logger.error("See this message?")
    captured: CaptureResult = capsys.readouterr()
    assert captured.out.startswith("ERROR")

    logger.critical("See this message?")
    captured: CaptureResult = capsys.readouterr()
    assert captured.out.startswith("CRITICAL")
