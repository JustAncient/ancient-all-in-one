"""Logging setup for diagnostics and support."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from ancient_all_in_one.config import LOG_FILE

LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"


def setup_logging(log_file: Path = LOG_FILE) -> None:
    """Configure rotating file logging once for the application."""

    root_logger = logging.getLogger()
    if root_logger.handlers:
        return

    log_file.parent.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(
        log_file,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    handler.setFormatter(logging.Formatter(LOG_FORMAT))

    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)
