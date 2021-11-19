from functools import wraps

import conreq


def manage_users_component() -> None:
    """Changes the manage users component."""

    def decorator(func):

        conreq.config.manage_users_component = func

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapped_func

    return decorator


def server_settings_component() -> None:
    """Changes the server settings component."""

    def decorator(func):

        conreq.config.server_settings_component = func

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapped_func

    return decorator
