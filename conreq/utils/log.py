"""Conreq Logging: Simplified logging module."""
import logging
from logging import Logger
from traceback import format_exc

# Globals
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

# Function reference to Py Logging getLogger
get_logger = logging.getLogger


def handler(msg: str, level: int, logger: Logger):
    """Submits a message to the log handler.

    Args:
        message: A string containing a verbose log message.
        logger: A logger objected obtained from get_logger().
        level: Logging module log level (ex. logging.WARNING)
    """
    # Remove trailing and proceeding whitespace from the message
    message = str(msg).rstrip("\n").rstrip().lstrip("\n").lstrip()

    # Log within a different stream depending on severity
    if level == DEBUG:
        logger.debug(message)
    elif level == INFO:
        logger.info(message)
    elif level == WARNING:
        logger.warning(message)
    elif level == ERROR:
        logger.error(message + "\n" + format_exc())
    elif level == CRITICAL:
        logger.critical(message + "\n" + format_exc())
