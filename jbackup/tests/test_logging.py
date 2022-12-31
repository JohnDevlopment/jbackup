from ..logging import new_logger, Level
import pytest

@pytest.mark.parametrize('level', list(Level))
def test_logger(level: Level):
    logger = new_logger('test logger', level)
    logger.debug('logging level is %s', level)
    logger.info('logging level is %s', level)
    logger.warn('logging level is %s', level)
    logger.error('logging level is %s', level)
    logger.critical('logging level is %s', level)
