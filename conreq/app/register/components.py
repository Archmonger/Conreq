from functools import wraps

# TODO: Create these functions
# pylint: disable=unused-argument,unused-variable,unnecessary-pass


def manage_users_component() -> None:
    """Changes the manage users component."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)


def server_settings_component() -> None:
    """Changes the server settings component."""

    def decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)
