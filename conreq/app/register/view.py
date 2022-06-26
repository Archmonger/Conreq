from typing import Any

from conreq import config

# pylint: disable=import-outside-toplevel


def landing() -> None:
    """Changes the home view."""

    def decorator(func):
        from conreq.utils.profiling import profiled_view

        config.views.landing = profiled_view(func)
        return func

    return decorator


def home() -> None:
    """Changes the home view."""

    def decorator(func):
        from conreq.utils.profiling import profiled_view

        config.views.home = profiled_view(func)
        return func

    return decorator


def sign_up() -> None:
    """Changes the sign up view."""

    def decorator(func):
        from conreq.utils.profiling import profiled_view

        config.views.sign_up = profiled_view(func)
        return func

    return decorator


def sign_in() -> None:
    """Changes the sign in view."""

    def decorator(func):
        from conreq.utils.profiling import profiled_view

        config.views.sign_in = profiled_view(func)
        return func

    return decorator


def password_reset() -> None:
    """Changes the password reset view."""

    def decorator(func: Any):
        from conreq.utils.profiling import profiled_view

        config.views.password_reset = profiled_view(func)
        return func

    return decorator


def password_reset_sent() -> None:
    """Changes the password reset sent view."""

    def decorator(func):
        from conreq.utils.profiling import profiled_view

        config.views.password_reset_sent = profiled_view(func)
        return func

    return decorator


def password_reset_confirm() -> None:
    """Changes the password reset confirm view."""

    def decorator(func):
        from conreq.utils.profiling import profiled_view

        config.views.password_reset_confirm = profiled_view(func)
        return func

    return decorator


def offline() -> None:
    """Changes the offline view."""

    def decorator(func):
        from conreq.utils.profiling import profiled_view

        config.views.offline = profiled_view(func)
        return func

    return decorator


def service_worker() -> None:
    """Changes the service worker view."""

    def decorator(func):
        from conreq.utils.profiling import profiled_view

        config.views.service_worker = profiled_view(func)
        return func

    return decorator


def web_manifest() -> None:
    """Changes the webmanifest view."""

    def decorator(func):
        from conreq.utils.profiling import profiled_view

        config.views.web_manifest = profiled_view(func)
        return func

    return decorator
