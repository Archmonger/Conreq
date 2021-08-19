"""Modifies the start behavior of Conreq, primarily related to conreq/settings.py"""

from functools import wraps

# TODO: Create these functions
# pylint: disable=unused-argument,unused-variable,unnecessary-pass


def pre_run(admin_required: bool = False):
    """Decorates any function that needs to be run prior to the webserver being up, but after Django has been configured."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)


def pre_startup():
    """Decorates any function that needs to be run prior to Django has been configured."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)


def setting(name, value):
    """Creates or modifies a variable in settings.py"""
    pass


def installed_app(path: str):
    """Adds a something to Django's "installed app" list in settings.py."""
    pass


def middleware(
    path: str,
    positioning_element: str = None,
    position_after: bool = True,
    default_position_to_end: bool = True,
):
    """Adds a middleware component in settings.py."""
    pass


def landing_page(template):
    """Changes the landing page variable in settings.py"""
    pass


def sign_up_page(template):
    """Changes the sign up page variable in settings.py"""
    pass


def sign_in_page(template):
    """Changes the sign in page variable in settings.py"""
    pass


def home_page(template):
    """Changes the home page variable in settings.py"""
    pass
