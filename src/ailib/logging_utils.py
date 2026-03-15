import logging
import os
import sys
from logging.handlers import RotatingFileHandler


logger = logging.getLogger("ailib")
logger.addHandler(logging.NullHandler())


def setup_logging(log_file=None, level=None, use_stderr=True, max_bytes=5 * 1024 * 1024, backup_count=3):
    log_level = (level or os.getenv("AILIB_LOG_LEVEL", "INFO")).upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    formatter = logging.Formatter("[%(asctime)s][%(name)s] %(levelname)s: %(message)s")

    file_target = log_file or os.getenv("AILIB_LOG_FILE")
    if file_target and not any(
        isinstance(handler, RotatingFileHandler) and getattr(handler, "baseFilename", None) == os.path.abspath(file_target)
        for handler in logger.handlers
    ):
        file_handler = RotatingFileHandler(
            file_target,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    wants_stderr = use_stderr and os.getenv("AILIB_LOG_STDERR", "true").lower() == "true"
    if wants_stderr and not any(
        isinstance(handler, logging.StreamHandler) and getattr(handler, "stream", None) is sys.stderr
        for handler in logger.handlers
    ):
        stream_handler = logging.StreamHandler(sys.stderr)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
