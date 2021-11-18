from functools import wraps

import conreq

# pylint: disable=import-outside-toplevel


def landing_view() -> None:
    """Changes the home view."""

    def decorator(func):

        from conreq.utils.profiling import metrics

        conreq.config.landing_view = metrics()(func)

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)

    return decorator


def home_view() -> None:
    """Changes the home view."""

    def decorator(func):

        from conreq.utils.profiling import metrics

        conreq.config.home_view = metrics()(func)

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)

    return decorator


def sign_up_view() -> None:
    """Changes the sign up view."""

    def decorator(func):

        from conreq.utils.profiling import metrics

        conreq.config.sign_up_view = metrics()(func)

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)

    return decorator


def sign_in_view() -> None:
    """Changes the sign in view."""

    def decorator(func):

        from conreq.utils.profiling import metrics

        conreq.config.sign_in_view = metrics()(func)

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)

    return decorator


def password_reset_view() -> None:
    """Changes the password reset view."""

    def decorator(func):

        from conreq.utils.profiling import metrics

        conreq.config.password_reset_view = metrics()(func)

        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return _wrapped_func(*args, **kwargs)

    return decorator
