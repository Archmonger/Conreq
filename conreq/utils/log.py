"""Conreq Logging: Simplified logging module."""
import logging
from traceback import format_exc

# Globals
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

# Function reference to Py Logging getLogger
get_logger = logging.getLogger


def handler(msg, level, logger):
    """Submits a message to the log handler.

    Args:
        message: A string containing a verbose log message.
        logger: A logger objected obtained from logging.getLogger().
        level: Logging module log level (ex. logging.WARNING)
    """
    # Remove trailing whitespace from the message
    message = str(msg).rstrip()

    # Log within a different stream depending on severity
    if level == DEBUG:
        logger.debug(message)
    if level == INFO:
        logger.info(message)
    if level == WARNING:
        logger.warning(message)
    if level == ERROR:
        logger.error(message + "\n" + format_exc())
    if level == CRITICAL:
        logger.critical(message + "\n" + format_exc())
