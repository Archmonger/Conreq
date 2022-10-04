"""Modifies the start behavior of Conreq, primarily related to conreq/settings.py."""

import logging
from multiprocessing import Process

from conreq import config

_logger = logging.getLogger(__name__)


def function(func):
    """Decorates any function that needs to be run prior to the webserver being up."""
    config.startup.functions.add(func)
    return func


def process(process: Process, no_warn: bool = False):
    """Any `Process` that needs to be run separately from Conreq during startup.
    Only one process will be created, regardless of how many webserver workers exist.
    """
    if not process.daemon and not no_warn:
        _logger.warning(
            "\033[93m"
            'Process "%s" is not a daemon, and thus may become a zombie if not properly handled.'
            "\033[0m",
            process.name,
        )
    config.startup.processes.add(process)
