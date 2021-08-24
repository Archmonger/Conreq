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


def setting_script(file_path: str) -> None:
    """Runs a file in settings.py. See django-split-settings for more details."""
    pass


def installed_app(path: str) -> None:
    """Shortcut to add an installed app to Django."""
    pass


def middleware(
    path: str,
    positioning_element: str = None,
    position_after: bool = True,
    default_position_to_end: bool = True,
) -> None:
    """Shortcut to add middleware to Django."""
    pass


def landing_template(template: str) -> None:
    """Changes the landing page variable."""
    pass


def landing_view() -> None:
    """Changes the home view."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)


def home_template(template: str) -> None:
    """Changes the home page variable."""
    pass


def home_view() -> None:
    """Changes the home view."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)


def sign_up_template(template: str) -> None:
    """Changes the sign up page variable."""
    pass


def sign_up_view() -> None:
    """Changes the sign up view."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)


def sign_in_template(template: str) -> None:
    """Changes the sign in page variable."""
    pass


def sign_in_view() -> None:
    """Changes the sign in view."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)


def password_reset_template(template: str) -> None:
    """Changes the password reset page variable."""
    pass


def password_reset_view() -> None:
    """Changes the password reset view."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)


def manage_users_component() -> None:
    """Changes the manage users component."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)
