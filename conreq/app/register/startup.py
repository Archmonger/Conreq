"""Modifies the start behavior of Conreq, primarily related to conreq/settings.py."""

from functools import wraps

# TODO: Create these functions
# pylint: disable=unused-argument,unused-variable,unnecessary-pass


def pre_run(admin_required: bool = False) -> object:
    """Decorates any function that needs to be run prior to the webserver being up, but after Django has been configured."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)

    return decorator


def setting_script(file_path: str) -> None:
    """Runs a file in settings.py. See django-split-settings for more details."""
    pass


def installed_app(path: str) -> None:
    """Shortcut to add an installed app to Django."""
    pass


def middleware(
    path: str,
    positioning_element: str = None,
    position_bottom: bool = True,
) -> None:
    """Shortcut to add middleware to Django."""
    pass
