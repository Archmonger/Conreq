"""Modifies the start behavior of Conreq, primarily related to conreq/settings.py."""

from functools import wraps
from typing import Callable

import conreq


def pre_run() -> Callable:
    """Decorates any function that needs to be run prior to the webserver being up."""

    def decorator(func):

        conreq.config.pre_run.add(func)

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapped_func

    return decorator


def setting_script(dotted_path: str) -> None:
    """
    Runs a file within settings.py. Wildcards are accepted.
    See django-split-settings docs for more details.
    """
    conreq.config.setting_scripts.add(dotted_path)


def installed_app(dotted_path: str) -> None:
    """Shortcut to add an installed app to Django."""
    conreq.config.installed_apps.add(dotted_path)
