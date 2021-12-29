from functools import wraps

from conreq import config


def manage_users() -> None:
    """Changes the manage users component."""

    def decorator(func):
        config.components.manage_users = func
        return func

    return decorator


def server_settings() -> None:
    """Changes the server settings component."""

    def decorator(func):
        config.components.server_settings = func
        return func

    return decorator


def user_settings() -> None:
    """Changes the user settings component."""

    def decorator(func):
        config.components.user_settings = func
        return func

    return decorator


def app_store() -> None:
    """Changes the app store component."""

    def decorator(func):
        config.components.app_store = func
        return func

    return decorator


def loading_animation() -> None:
    """Changes the default component loading animation."""

    def decorator(func):
        config.components.loading_animation = func
        return func

    return decorator
