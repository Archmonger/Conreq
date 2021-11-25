from functools import wraps
from typing import Any

import conreq
from conreq.utils.profiling import profiled_view

# pylint: disable=import-outside-toplevel


def landing_view() -> None:
    """Changes the home view."""

    def decorator(func):
        conreq.config.landing_view = profiled_view(func)

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapped_func

    return decorator


def home_view() -> None:
    """Changes the home view."""

    def decorator(func):
        conreq.config.home_view = profiled_view(func)

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapped_func

    return decorator


def sign_up_view() -> None:
    """Changes the sign up view."""

    def decorator(func):
        conreq.config.sign_up_view = profiled_view(func)

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapped_func

    return decorator


def sign_in_view() -> None:
    """Changes the sign in view."""

    def decorator(func):
        conreq.config.sign_in_view = profiled_view(func)

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapped_func

    return decorator


def password_reset_view() -> None:
    """Changes the password reset view."""

    def decorator(func: Any):
        conreq.config.password_reset_view = profiled_view(func)

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapped_func

    return decorator


def password_reset_sent_view() -> None:
    """Changes the password reset view."""

    def decorator(func):
        conreq.config.password_reset_sent_view = profiled_view(func)

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapped_func

    return decorator
