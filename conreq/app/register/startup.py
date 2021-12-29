"""Modifies the start behavior of Conreq, primarily related to conreq/settings.py."""

from functools import wraps
from typing import Callable

from conreq import config


def pre_run() -> Callable:
    """Decorates any function that needs to be run prior to the webserver being up."""

    def decorator(func):
        config.startup.pre_run.add(func)
        return func

    return decorator


def setting_script(dotted_path: str) -> None:
    """
    Runs a file within settings.py. Wildcards are accepted.
    See django-split-settings docs for more details.
    """
    config.startup.setting_scripts.add(dotted_path)


def installed_app(dotted_path: str) -> None:
    """Shortcut to add an installed app to Django."""
    config.startup.installed_apps.add(dotted_path)
