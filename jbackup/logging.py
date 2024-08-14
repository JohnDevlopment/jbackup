from __future__ import annotations
import logging
import logging.config
from pathlib import Path
from typing import Any

from platformdirs import user_log_path
import yaml

from . import APPNAME

def setup_logging():
    fp = Path(__file__).parent / "logging.yaml"
    with fp.open('rt') as fd:
        LOGGING_CONFIG: dict[str, Any] = yaml.safe_load(fd)
        LOGGING_CONFIG['handlers']['file']['filename'] = user_log_path(APPNAME) / "jbackup.log"
        logging.config.dictConfig(LOGGING_CONFIG)

    logging.getLogger(APPNAME).info("Setup logging configuration")
