"""Conreq Logging: Simplified logging module."""
import logging
import os
from traceback import format_exc

# TODO: Obtain these values from the database on init
LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

# TODO: Obtain this DATA_DIR from the database on init. LOGS_DIR exists within DATA_DIR.
__LOGS_DIR = "logs"
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


def logger_format(logger, formatting):
    """Sets the log format to be used for the current logger and future logger instances.
    For formatting information, see logging.Formatter()

    Args:
        logger: A logger objected obtained from logging.getLogger().
        formatting: String containing Logging module format
    """
    # TODO: Change this to a database save
    global LOG_FORMAT
    LOG_FORMAT = formatting

    # Configure the output format
    formatter = logging.Formatter(LOG_FORMAT)

    # Configure the logger's output format
    for handle in logger.handlers:
        handle.setFormatter(formatter)


def console_stream(logger, level):
    """Creates a console output stream for a logger instance.

    Args:
        logger: A logger objected obtained from logging.getLogger().
        level: Logging module log level (ex. logging.WARNING)
    """
    # Remove old stream handler
    for handle in logger.handlers[:]:
        if isinstance(handle, logging.StreamHandler):
            logger.removeHandler(handle)

    # Configure new stream handler
    formatter = logging.Formatter(LOG_FORMAT)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
