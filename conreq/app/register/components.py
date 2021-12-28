from functools import wraps

from conreq import config


# TODO: Add all the other component types in here
def manage_users_component() -> None:
    """Changes the manage users component."""

    def decorator(func):

        config.components.manage_users = func

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapped_func

    return decorator


def server_settings_component() -> None:
    """Changes the server settings component."""

    def decorator(func):

        config.components.server_settings = func

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapped_func

    return decorator
