"""Modifies the start behavior of Conreq, primarily related to conreq/settings.py."""

from functools import wraps
from typing import Callable

from conreq import app


def pre_run() -> Callable:
    """Decorates any function that needs to be run prior to the webserver being up."""

    def decorator(func):

        app.config.pre_run.append(func)

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)

    return decorator


def setting_script(path: str) -> None:
    """Runs a file in settings.py. See django-split-settings for more details."""
    app.config.setting_scripts.append(path)


def installed_app(path: str) -> None:
    """Shortcut to add an installed app to Django."""
    app.config.installed_apps.append(path)


def middleware(
    path: str,
    positioning_element: str = None,
    position_below: bool = True,
) -> None:
    """Shortcut to add middleware to Django."""
    app.config.middlewares.append(
        {
            "path": path,
            "pos_elem": positioning_element,
            "below": position_below,
        }
    )
