"""Conreq Logging: Simplified logging module."""
import logging
import os
from traceback import format_exc

# Globals
LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

__DATA_DIR = os.environ.get("DATA_DIR", "")
if __DATA_DIR != "" and not __DATA_DIR.endswith("/"):
    __DATA_DIR = __DATA_DIR + "/"

__LOGS_DIR = __DATA_DIR + "logs"
if not os.path.exists(__LOGS_DIR):
    os.mkdir(__LOGS_DIR)

logging.basicConfig(
    filename=os.path.join(__LOGS_DIR, "conreq.log"),
    format=LOG_FORMAT,
    level=logging.WARNING,
)

# Function reference to Py Logging getLogger
get_logger = logging.getLogger


def handler(message, level, logger):
    """Submits a message to the log handler.

    Args:
        message: A string containing a verbose log message.
        logger: A logger objected obtained from logging.getLogger().
        level: Logging module log level (ex. logging.WARNING)
    """
    # Remove trailing whitespace from the message
    message = message.rstrip()

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


def configure(logger, level):
    """Configures or re-configures a logger instance for application logging.

    Args:
        logger: A logger objected obtained from logging.getLogger().
        level: Logging module log level (ex. logging.WARNING)
    """
    # Configure the root logger
    if logger == logging.getLogger():
        # Configure the logger's minimum level
        for handle in logger.handlers:
            handle.setLevel(level)

    # Configure a child logger
    else:
        # Remove all handles (log messages go to root through propogation)
        for handle in logger.handlers[:]:
            logger.removeHandler(handle)

        # Configure the logger's minimum level
        logger.setLevel(level)


def console_stream(logger, level):
    """Creates a console output stream for a logger instance.

    Args:
        logger: A logger objected obtained from logging.getLogger().
        level: Logging module log level (ex. logging.WARNING)
    """
    # Configure new stream handler
    formatter = logging.Formatter(LOG_FORMAT)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
