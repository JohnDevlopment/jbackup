from __future__ import annotations
from ..logging import get_logger, Level
from typing import NamedTuple

class CaptureResult(NamedTuple):
    out: str
    err: str

def test_logger(capsys):
    logger = get_logger('tests.logging', Level.DEBUG)

    capsys.readouterr()

    logger.debug("See this message?")
    captured: CaptureResult = capsys.readouterr()
    assert captured.out.startswith("DEBUG"), f"does not start with \"DEBUG\" ({captured.out!r})"

    logger.info("See this message?")
    captured: CaptureResult = capsys.readouterr()
    assert captured.out.startswith("INFO"), f"does not start with \"INFO\" ({captured.out!r})"

    logger.warn("See this message?")
    captured: CaptureResult = capsys.readouterr()
    assert captured.out.startswith("WARN"), f"does not start with \"WARN\" ({captured.out!r})"

    logger.error("See this message?")
    captured: CaptureResult = capsys.readouterr()
    assert captured.out.startswith("ERROR"), f"does not start with \"ERROR\" ({captured.out!r})"

    logger.critical("See this message?")
    captured: CaptureResult = capsys.readouterr()
    assert captured.out.startswith("CRITICAL"), f"does not start with \"CRITICAL\" ({captured.out!r})"

    assert logger.name != ''
