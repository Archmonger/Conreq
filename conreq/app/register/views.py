from functools import wraps
from typing import Any

import conreq

# pylint: disable=import-outside-toplevel


def landing_view() -> None:
    """Changes the home view."""

    def decorator(func):
        from conreq.utils.profiling import profiled_view

        conreq.config.landing_view = profiled_view(func)

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapped_func

    return decorator


def home_view() -> None:
    """Changes the home view."""

    def decorator(func):
        from conreq.utils.profiling import profiled_view

        conreq.config.home_view = profiled_view(func)

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapped_func

    return decorator


def sign_up_view() -> None:
    """Changes the sign up view."""

    def decorator(func):
        from conreq.utils.profiling import profiled_view

        conreq.config.sign_up_view = profiled_view(func)

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapped_func

    return decorator


def sign_in_view() -> None:
    """Changes the sign in view."""

    def decorator(func):
        from conreq.utils.profiling import profiled_view

        conreq.config.sign_in_view = profiled_view(func)

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapped_func

    return decorator


def password_reset_view() -> None:
    """Changes the password reset view."""

    def decorator(func: Any):
        from conreq.utils.profiling import profiled_view

        conreq.config.password_reset_view = profiled_view(func)

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapped_func

    return decorator


def password_reset_sent_view() -> None:
    """Changes the password reset sent view."""

    def decorator(func):
        from conreq.utils.profiling import profiled_view

        conreq.config.password_reset_sent_view = profiled_view(func)

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapped_func

    return decorator


def password_reset_confirm_view() -> None:
    """Changes the password reset confirm view."""

    def decorator(func):
        from conreq.utils.profiling import profiled_view

        conreq.config.password_reset_confirm_view = profiled_view(func)

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapped_func

    return decorator
